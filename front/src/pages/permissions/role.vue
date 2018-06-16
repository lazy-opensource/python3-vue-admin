<template>
  <el-container>
    <el-header height="50">
      <el-form :inline="true" :model="roleSearchForm" size="mini" class="demo-form-inline">
        <el-form-item label="角色名称">
          <el-input v-model="roleSearchForm.role_name" placeholder="角色名称"></el-input>
        </el-form-item>
        <el-form-item label="角色编码">
          <el-input v-model="roleSearchForm.role_code" placeholder="角色编码"></el-input>
        </el-form-item>
        <el-form-item label="修改时间">
          <el-date-picker
            v-model="roleSearchForm._s_last_update_time"
            type="date"
            :editable=false
            format="yyyy 年 MM 月 dd 日"
            value-format="yyyy-MM-dd"
            size="mini"
            placeholder="开始时间">
          </el-date-picker>
        </el-form-item>
        <el-form-item label="修改时间">
          <el-date-picker
            :editable=false
            format="yyyy 年 MM 月 dd 日"
            value-format="yyyy-MM-dd"
            v-model="roleSearchForm._e_last_update_time"
            type="date"
            size="mini"
            placeholder="结束时间">
          </el-date-picker>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="onSearch">查询</el-button>
          <el-button type="info" @click="onClean">清空</el-button>
          <el-button type="success" @click="onAdd">新增</el-button>
          <el-button type="warning" @click="onRelGroup">关联用户组</el-button>
          <el-button type="danger" @click="onDelete">删除</el-button>
        </el-form-item>
      </el-form>
    </el-header>
    <el-main>
      <el-table
        :data="roleTableData"
        ref="roleMultipleTable"
        @selection-change="onSelectionChange"
        @select="listenerSelect"
        @select-all="listenerSelect"
        :default-sort="{prop: 'last_update_time', order: 'descending'}"
        border max-height="360" style="width: 100%">
        <el-table-column type="selection" width="40"></el-table-column>
        <el-table-column prop="role_name" align="left" label="角色名称" width="150"></el-table-column>
        <el-table-column prop="role_code" align="left" label="角色编码" width="150"></el-table-column>
        <el-table-column prop="valid_status" align="left" label="启用状态" width="150"
                         :formatter="formatterValidStatus"></el-table-column>
        <el-table-column prop="create_time" align="left" :formatter="formatterDate" label="创建日期"
                         width="150"></el-table-column>
        <el-table-column prop="last_update_time" align="left" :formatter="formatterDate" sortable
                         label="最后修改日期"></el-table-column>
        <el-table-column fixed="right" align="left" width="250px;" label="操作">
          <template slot-scope="scope">
            <el-button size="mini" @click="onEdit(scope.$index, scope.row)">编辑</el-button>
            <el-button size="mini" type="info" @click="onRelResource(scope.$index, scope.row)">关联资源</el-button>
            <el-button size="mini" type="danger" @click="onDelete(scope.$index, scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-dialog title="编辑信息" :visible.sync="dialogVisible" :show-close="false" width="40%">
        <el-form :model="roleEditForm" status-icon :rules="roleEditFormRule" ref="roleEditForm"
                 label-width="100px" class="demo-ruleForm">
          <el-form-item label="角色名称" prop="role_name">
            <el-input type="text" v-model="roleEditForm.role_name" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="角色编码" prop="role_code">
            <el-input type="text" v-model.number="roleEditForm.role_code" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="启用状态">
            <el-select v-model="roleEditForm.valid_status" placeholder="启用状态">
              <el-option label="--请选择--" value=""></el-option>
              <el-option label="启用" value="Y"></el-option>
              <el-option label="停用" value="N"></el-option>
            </el-select>
          </el-form-item>
        </el-form>
        <span slot="footer" class="dialog-footer">
          <el-button @click="cancelEdit">取 消</el-button>
          <el-button @click="resetEdit">重 置</el-button>
          <el-button type="primary" @click="saveOrUpdate">确 定</el-button>
        </span>
      </el-dialog>

      <!--关联用户组-->
      <el-dialog title="关联用户组" :visible.sync="relGroupDialogVisible" width="80%"
                 :before-close="relGroupDialogClose">
        <el-container>
          <el-main>
            <div class="custom-tree-container">
              <div class="block">
                <el-input
                  placeholder="输入关键字进行过滤"
                  v-model="relGroupFilterText">
                </el-input>
                <el-tree
                  class="filter-tree"
                  show-checkbox
                  check-strictly
                  node-key="id"
                  :expand-on-click-node="false"
                  :data="relGroupData"
                  :props="relGroupDefaultProps"
                  default-expand-all
                  :filter-node-method="relGroupFilterNode"
                  ref="relGroupRef">
                </el-tree>
              </div>
            </div>
            <el-footer height="50" style="margin-bottom: 5px;">
              <el-button type="primary" size="mini" @click="relGroupConfirm">确定关联</el-button>
            </el-footer>
          </el-main>
        </el-container>
      </el-dialog>

      <!--关联资源权限-->
      <el-dialog title="关联资源权限" :visible.sync="relResourceDialogVisible" width="80%"
                 :before-close="handleRelResourcesDialogClose">
        <el-container>
          <el-main>
            <div class="custom-tree-container">
              <div class="block">
                <el-input
                  placeholder="输入关键字进行过滤"
                  v-model="relResourceFilterText">
                </el-input>
                <el-tree
                  class="filter-tree"
                  show-checkbox
                  node-key="id"
                  :expand-on-click-node="false"
                  :data="relResourceData"
                  :props="relResourceDefaultProps"
                  default-expand-all
                  :filter-node-method="relResourceFilterNode"
                  ref="relResourceRef">
                </el-tree>
              </div>
            </div>
          </el-main>
          <el-footer height="50" style="margin-top: 10px;">
            <el-button type="primary" size="mini" @click="relResourceConfirm">关联资源</el-button>
          </el-footer>
        </el-container>
      </el-dialog>

    </el-main>
    <el-footer>
      <div class="block">
        <el-pagination
          @size-change="onChangePageSize"
          @current-change="onChangeCurrentPage"
          :current-page.sync="roleSearchForm.paging.current_page"
          :page-sizes="[5, 10, 20, 50]"
          :page-size="roleSearchForm.paging.page_size"
          layout="total, sizes, prev, pager, next, jumper"
          :total="totalNum">
        </el-pagination>
      </div>
    </el-footer>
  </el-container>
</template>

<script>
  import * as Constant from "../../constant";
  import Utils from "../../utils";
  import ElFooter from "element-ui/packages/footer/src/main";

  export default {
    components: {ElFooter},
    methods: {

      ///////////////////////////////     关联用户组   /////////////////////
      //点击关联用户组
      onRelGroup() {
        let self = this;
        if (this.roleMultipleSelection.length !== 1) {
          self.$message('请选择一项进行操作');
          return false;
        }
        self.relGroupDialogVisible = true;
        //查当前用户所在的用户组数据
        self.$axios.get(
          Constant.ADMIN_PERMISSIONS_ROLE_GROUPS,
          {
            params: {
              params: {
                role_id: self.roleMultipleSelection[0].id
              }
            }
          }
        ).then(function (resp) {
          if (resp.code !== Constant.REQ_SUCCESS) {
            self.$message({type: 'error', message: resp.msg});
            return false;
          }
          let current_groups = resp.data;
          let keys = [];
          for (let i in current_groups) {
            keys.push(current_groups[i]);
          }
          self.$refs.relGroupRef.setCheckedKeys(keys, false);
        }).catch(resp => {
          console.log(resp);
          self.$message({type: 'error', message: '系统错误'});
        });
      },
      //查看/编辑资源权限关闭对话框回调
      relGroupDialogClose() {
        this.$refs.relGroupRef.setCheckedKeys([]);
        this.relGroupDialogVisible = false;
      },
      //关联用户组过滤
      relGroupFilterNode(value, data) {
        if (!value) return true;
        return data.label.indexOf(value) !== -1;
      },
      //用户组查询
      relGroupOnSearch() {
        let self = this;
        this.$axios({
          method: 'get',
          url: Constant.ADMIN_PERMISSIONS_GROUPS_URI
        }).then(function (resp) {
          if (resp.code !== Constant.REQ_SUCCESS) {
            self.$alert(resp.msg, '系统提示');
          } else {
            self.relGroupData = resp.data.rows;
          }
          self.loading = false;
        }).catch(resp => {
          console.log(resp);
          self.$alert('请求出错', '系统提示');
          self.loading = false;
        });
      },
      //确定关联用户组
      relGroupConfirm() {
        let self = this;
        let allCheck = self.$refs.relGroupRef.getCheckedKeys();
        this.$confirm('确定关联用户组吗?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          self.$axios.post(Constant.ADMIN_PERMISSIONS_ROLE_GROUPS, {
            params: {
              group_ids: allCheck,
              role_id: self.roleMultipleSelection[0].id
            }
          }).then(function (resp) {
            if (resp.code === Constant.REQ_SUCCESS) {
              self.$message({type: 'success', message: '关联用户组成功!'});
              self.cleanAllSelect();
              self.relGroupDialogClose();
            } else {
              self.$message({type: 'error', message: resp.msg});
            }
          }).catch(resp => {
            console.log(resp);
            self.$message({type: 'error', message: '服务器错误'});
          });
        }).catch(() => {
          self.$message({type: 'info', message: '已取消删除'});
        });
      },
      ///////////////////////////////     关联用户组   /////////////////////


      ///////////////////////////////     关联资源权限 Start  /////////////////////
      relResourceConfirm() {
        let self = this;
        let allCheck = self.$refs.relResourceRef.getCheckedKeys();
        let halfCheck = self.$refs.relResourceRef.getHalfCheckedKeys();
        if (allCheck && halfCheck) {
          allCheck = allCheck.concat(halfCheck);
        } else if (halfCheck) {
          allCheck = halfCheck;
        }
        this.$confirm('确定关联资源吗?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          self.$axios.post(Constant.ADMIN_PERMISSIONS_ROLE_RESOURCES, {
            params: {
              role_id : self.rel_resource_role_id,
              res_ids: allCheck
            }
          }).then(function (resp) {
            if (resp.code === Constant.REQ_SUCCESS) {
              // self.viewOrEditOnSearch(self.edit_resource_group_id, self);
              self.$message({type: 'success', message: '分配资源成功!'});
              self.handleRelResourcesDialogClose();
            } else {
              self.$message({type: 'error', message: resp.msg});
            }
          }).catch(resp => {
            console.log(resp);
            self.$message({type: 'error', message: '服务器错误'});
          });
        }).catch(() => {
          self.$message({type: 'info', message: '已取消'});
        });
      },
      onRelResource(node, data) {
        this.relResourceDialogVisible = true;
        this.rel_resource_role_id = data.id;
        this.loadRelResourceData(data.id);
      },
      //查看/编辑资源权限关闭对话框回调
      handleRelResourcesDialogClose() {
        this.$refs.relResourceRef.setCheckedKeys([]);
        this.relResourceDialogVisible = false;
      },
      //过滤关联资源
      relResourceFilterNode(value, data) {
        if (!value) return true;
        return data.label.indexOf(value) !== -1;
      },
      //初始化查看编辑资源对话框树
      loadRelResourceData(roleId) {
        let self = this;
        self.$axios.get(Constant.ADMIN_PERMISSIONS_ROLE_RESOURCES, {
          params: {
            params: {
              role_id: roleId
            }
          }
        }).then(function (res) {
          if (res.code !== Constant.REQ_SUCCESS) {
            self.$message({type: 'error', message: res.msg});
          } else {
            self.relResourceData = res.data.all_can_rel_rows;
            let aleary_rel_rows = res.data.aleary_rel_rows;
            let keys = [];
            for (let i in aleary_rel_rows) {
              keys.push(aleary_rel_rows[i]);
            }
            self.$refs.relResourceRef.setCheckedKeys(keys, false);
          }
        }).catch(function (res) {
          console.log(res);
          self.$message({type: 'error', message: '系统错误'});
        })
      },
      ///////////////////////////////     关联资源权限 End  /////////////////////

      ///////////////////////////////     角色列表 Start   /////////////////////
      //查询
      onSearch() {
        let self = this;
        this.$axios({
          method: 'get',
          url: Constant.ADMIN_PERMISSIONS_ROLES_URI,
          params: {
            params: this.roleSearchForm
          }
        }).then(function (resp) {
          if (resp.code !== Constant.REQ_SUCCESS) {
            self.$alert(resp.msg, '系统提示');
          } else {
            self.totalNum = resp.data.total;
            self.roleTableData = resp.data.rows;
          }
        }).catch(resp => {
          console.log(resp);
          self.$alert('请求出错', '系统提示');
        });
      },

      //触发删除事件
      onDelete(index, row) {
        let self = this;
        if (!row && this.roleMultipleSelection.length < 1) {
          this.$message('请至少选择一项进行操作');
          return;
        } else {
          if (row && row.can_edit === 'N') {
            this.$message({type: 'info', message: row.role_name + '是系统数据不可编辑'});
            return;
          }
        }
        this.$confirm('此操作将永久删除文件, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          let deleteIds = [];
          if (row) {
            deleteIds.push(row.id);
          } else {
            for (let index in this.roleMultipleSelection) {
              deleteIds.push(this.roleMultipleSelection[index].id);
            }
          }
          this.$axios.delete(Constant.ADMIN_PERMISSIONS_ROLES_URI, {
            params: {
              ids: JSON.stringify(deleteIds)
            }
          }).then(function (resp) {
            if (resp.code === Constant.REQ_SUCCESS) {
              self.onSearch();
              self.$message({type: 'success', message: '删除成功!'});
            } else {
              self.$message({type: 'error', message: resp.msg});
            }
          }).catch(resp => {
            self.$message({type: 'error', message: '服务器错误'});
          });
        }).catch(() => {
          self.$message({type: 'info', message: '已取消删除'});
        });
      },

      //取消编辑
      cancelEdit() {
        this.resetEdit();
        this.dialogVisible = false;
      },

      //重置按钮
      resetEdit() {
        this.roleEditForm.id = '';
        this.roleEditForm.role_name = '';
        this.roleEditForm.role_code = '';
        this.roleEditForm.valid_status = 'Y';
      },
      /**
       * 新增、修改
       */
      saveOrUpdate() {
        let self = this;
        this.$refs['roleEditForm'].validate((valid) => {
          if (valid) {
            self.$axios.get(Constant.ADMIN_PERMISSIONS_ROLE_CHECK_UNIQ, {
              params: {
                params: {
                  role_name: self.roleEditForm.role_name,
                  rule: {
                    role_name: 'eq'
                  }
                }
              }
            }).then(function (res) {
              if (res.code === Constant.REQ_SUCCESS) {
                if (res.data && res.data.length > 0 && (res.data[0].id !== self.roleEditForm.id)) {
                  self.$message({type: 'info', message: '角色名称重复，请重新设置'});
                  return false;
                }
                self.$axios.get(Constant.ADMIN_PERMISSIONS_ROLE_CHECK_UNIQ, {
                  params: {
                    params: {
                      role_code: self.roleEditForm.role_code,
                      rule: {
                        role_name: 'eq'
                      }
                    }
                  }
                }).then(function (res) {
                  if (res.code === Constant.REQ_SUCCESS) {
                    if (res.data && res.data.length > 0 && (res.data[0].id !== self.roleEditForm.id)) {
                      self.$message({type: 'info', message: '角色编码重复，请重新设置'});
                      return false;
                    }
                    if (self.roleEditForm.id) {
                      self.$axios.post(Constant.ADMIN_PERMISSIONS_ROLES_URI, {
                        params: self.roleEditForm
                      }).then(function (resp) {
                        if (resp.code === Constant.REQ_SUCCESS) {
                          self.onSearch();
                          self.$message({type: 'success', message: '修改成功!'});
                        } else {
                          self.$message({type: 'info', message: resp.msg});
                        }
                      }).catch(resp => {
                        console.log(resp);
                        self.$message({type: 'error', message: '系统错误'});
                      });
                    } else {
                      self.$axios.put(Constant.ADMIN_PERMISSIONS_ROLES_URI, {
                        params: self.roleEditForm
                      }).then(function (resp) {
                        if (resp.code === Constant.REQ_SUCCESS) {
                          self.onSearch();
                          self.$message({type: 'success', message: '添加成功!'});
                        } else {
                          self.$message({type: 'info', message: resp.msg});
                        }
                      }).catch(resp => {
                        self.$message({type: 'error', message: '系统错误'});
                      })
                    }
                    self.dialogVisible = false;
                  } else {
                    self.$message({type: 'info', message: res.msg});
                  }
                }).catch(resp => {
                  console.log(resp);
                  self.$message({type: 'error', message: '系统错误'});
                });
              } else {
                self.$message({type: 'info', message: res.msg});
              }
            }).catch(resp => {
              console.log(resp);
              self.$message({type: 'error', message: '系统错误'});
            });
          } else {
            self.$message({type: 'warning', message: '表单验证不通过'});
          }
        });
      },

      /**
       * 触发修改按钮
       * @param index
       * @param row
       */
      onEdit(index, row) {
        if (row && row.can_edit === 'N') {
          this.$message({type: 'info', message: row.role_name + '是系统数据不可编辑'});
          return;
        }
        this.roleEditForm.id = row.id;
        this.roleEditForm.role_name = row.role_name;
        this.roleEditForm.role_code = row.role_code;
        this.roleEditForm.valid_status = row.valid_status;
        this.dialogVisible = true;
      },

      /**
       * 触发修改页面条数事件
       */
      onChangePageSize(page_size) {
        this.roleSearchForm.paging.page_size = page_size;
        this.onSearch();
      },

      /**
       * 触发修改当前页事件
       */
      onChangeCurrentPage() {
        this.onSearch();
      },

      cleanAllSelect() {
        this.$refs.roleMultipleTable.clearSelection();
      },

      /**
       * 清除编辑表单
       */
      onClean() {
        this.roleSearchForm.role_name = '';
        this.roleSearchForm.role_code = '';
        this.roleSearchForm.valid_status = '';
        this.roleSearchForm._s_last_update_time = '';
        this.roleSearchForm._e_last_update_time = '';
      },

      /**
       * 触发新增按钮
       */
      onAdd() {
        this.resetEdit();
        this.dialogVisible = true;
      },

      /**
       * 格式化valid_status列
       * @param row
       * @param column
       * @param cellValue
       * @returns {string}
       */
      formatterValidStatus(row, column, cellValue) {
        if (cellValue === 'Y') {
          return '启用'
        } else {
          return '停用'
        }
      },

      formatterDate(row, column, cellValue) {
        return Utils.formatDate(new Date(cellValue), 'yyyy-MM-dd')
      },

      /**
       * 全选事件
       * @param rows
       */
      onSelectionChange(rows) {
        this.roleMultipleSelection = rows;
      },

      //监听选择时间
      listenerSelect(rows) {
        if (rows) {
          rows.forEach(row => {
            if (row.can_edit === 'N') {
              this.$refs.roleMultipleTable.toggleRowSelection(row, false);
            }
          });
        }
      }
    },

    /**
     * 监听器定义
     * **/
    watch: {
      //查看编辑资源过滤
      relResourceFilterText(val) {
        this.$refs.relResourceRef.filter(val);
      }
    },
    data() {
      let checkRoleCode = (rule, value, callback) => {
        if (!value) {
          return callback(new Error('请输入角色编码'));
        }
        if (value.length > 20) {
          return callback(new Error('长度不能大于20'));
        }
        if (value.length < 2) {
          return callback(new Error('长度不能小于2'));
        }
        callback();
      };
      let checkRoleName = (rule, value, callback) => {
        if (value === '') {
          return callback(new Error('请输入角色名称'));
        }
        if (value.length > 20) {
          return callback(new Error('名称长度不能大于20'));
        }
        if (value.length < 2) {
          return callback(new Error('长度不能小于2'));
        }
        callback();
      };
      return {
        ///////////////////////////////     关联用户组   /////////////////////
        relGroupDialogVisible: false,
        relGroupFilterText: '',
        relGroupData: [{}],
        relGroupDefaultProps: {
          children: 'children',
          label: 'label'
        },
        ///////////////////////////////     关联用户组   /////////////////////

        ///////////////////////////////     关联资源权限   /////////////////////
        relResourceDialogVisible: false,
        relResourceDetailsVisible: false,
        relResourceFilterText: '',
        groupData: [],
        defaultProps: {
          children: 'children',
          label: 'label'
        },
        relResourceData: [{}],
        rel_resource_role_id: '',
        relResourceDefaultProps: {
          children: 'children',
          label: 'label'
        },
        relResourceDetailsPopoverObj: {
          res_name: '',
          res_desc: '',
          res_uri: '',
          res_type: '',
          method: '',
          res_code: '',
        },
        ///////////////////////////////     关联资源权限   /////////////////////

        ///////////////////////////////     编辑角色   /////////////////////
        roleEditFormRule: {
          role_name: [
            {validator: checkRoleName, trigger: 'blur'}
          ],
          role_code: [
            {validator: checkRoleCode, trigger: 'blur'}
          ],
        },
        dialogVisible: false,
        roleEditForm: {
          id: '',
          role_name: '',
          pid: '-1',
          role_code: '',
          valid_status: 'Y',
        },
        ///////////////////////////////     编辑角色   /////////////////////
        roleMultipleSelection: [],
        roleSearchForm: {
          role_name: '',
          role_code: '',
          contact: '',
          valid_status: '',
          _s_last_update_time: '',
          _e_last_update_time: '',
          paging: {
            page_size: 5,
            current_page: 1
          },
          rule: {
            role_name: 'like',
            role_code: 'like',
            contact: 'like'
          }
        },
        totalNum: 100,
        roleTableData: [],
      }
    },

    /**
     * 计算属性定义
     */
    computed: {},

    mounted: function () {
      this.onSearch();
      this.relGroupOnSearch();
    },

    /**
     * 初始化钩子函数
     */
    created: function () {

    }
  }
</script>

<style scoped>
  .el-header {
    background-color: gainsboro;
    color: #333;
    padding: 0px;
    padding-top: 5px;
    text-align: left;
    line-height: 0px;
  }

  .el-main {
    background-color: #E9EEF3;
    color: #333;
    text-align: center;
    line-height: 0px;
    padding: 0px;
  }

  .el-footer {
    background-color: #E9EEF3;
    color: white;
    font-size: x-small;
    text-align: center;
    line-height: 0px;
    padding: 0px;
    padding-top: 20px;
  }
</style>
