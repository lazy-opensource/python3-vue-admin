<template>
  <el-container>
    <el-header height="50">
      <el-form :inline="true" :model="userSearchForm" size="mini" class="demo-form-inline">
        <el-form-item label="登录名称">
          <el-input v-model="userSearchForm.login_name" placeholder="登录名称"></el-input>
        </el-form-item>
        <el-form-item label="昵称">
          <el-input v-model="userSearchForm.nickname" placeholder="昵称"></el-input>
        </el-form-item>
        <el-form-item label="联系电话">
          <el-input v-model="userSearchForm.contact" placeholder="联系电话"></el-input>
        </el-form-item>

        <el-form-item label="启用状态">
          <el-select v-model="userSearchForm.valid_status" placeholder="启用状态">
            <el-option label="--请选择--" value=""></el-option>
            <el-option label="启用" value="Y"></el-option>
            <el-option label="停用" value="N"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="修改时间">
          <el-date-picker
            v-model="userSearchForm._s_last_update_time"
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
            v-model="userSearchForm._e_last_update_time"
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
        :data="userTableData"
        ref="userMultipleTable"
        @selection-change="onSelectionChange"
        @select="listenerSelect"
        @select-all="listenerSelect"
        :default-sort="{prop: 'last_update_time', order: 'descending'}"
        border max-height="360" style="width: 100%">
        <el-table-column type="selection" width="40"></el-table-column>
        <el-table-column prop="login_name" align="left" label="登录名称" width="150"></el-table-column>
        <el-table-column prop="nickname" align="left" label="昵称" width="150"></el-table-column>
        <el-table-column prop="contact" align="left" sortable label="联系电话" width="150"></el-table-column>
        <el-table-column prop="valid_status" align="left" label="启用状态" width="150"
                         :formatter="formatterValidStatus"></el-table-column>
        <el-table-column prop="create_time" align="left" :formatter="formatterDate" label="创建日期"
                         width="150"></el-table-column>
        <el-table-column prop="last_update_time" align="left" :formatter="formatterDate" sortable
                         label="最后修改日期"></el-table-column>
        <el-table-column fixed="right" align="left" width="250px;" label="操作">
          <template slot-scope="scope">
            <el-button size="mini" @click="onEdit(scope.$index, scope.row)">编辑</el-button>
            <el-button size="mini" type="info" @click="onRelRole(scope.$index, scope.row)">关联角色</el-button>
            <el-button size="mini" type="danger" @click="onDelete(scope.$index, scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-dialog title="编辑信息" :visible.sync="dialogVisible" :show-close="false" width="40%">
        <el-form :model="userEditForm" status-icon :rules="userEditFormRule" ref="userEditForm"
                 label-width="100px" class="demo-ruleForm">
          <el-form-item label="登录名称" prop="login_name">
            <el-input type="text" v-model="userEditForm.login_name" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="昵称" prop="nickname">
            <el-input type="text" v-model.number="userEditForm.nickname" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="联系电话" prop="contact">
            <el-input v-model="userEditForm.contact"></el-input>
          </el-form-item>
          <el-form-item label="密码" prop="password" v-if="!userEditForm.id">
            <el-input v-model="userEditForm.password"></el-input>
          </el-form-item>
          <el-form-item label="状态">
            <el-select v-model="userEditForm.valid_status" placeholder="状态">
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

      <!--关联角色-->
      <el-dialog title="关联角色" :visible.sync="relRoleDialogVisible" width="60%"
                 :before-close="handleRelRoleDialogClose">
        <el-container>
          <el-header height="50">
            <el-form :inline="true" :model="relRoleSearchForm" size="mini" class="demo-form-inline">
              <el-form-item label="角色名称">
                <el-input v-model="relRoleSearchForm.role_name" placeholder="角色名称"></el-input>
              </el-form-item>
              <el-form-item label="角色编码">
                <el-input v-model="relRoleSearchForm.role_code" placeholder="角色编码"></el-input>
              </el-form-item>
              <el-form-item label="启用状态">
                <el-select v-model="relRoleSearchForm.valid_status" placeholder="启用状态">
                  <el-option label="--请选择--" value=""></el-option>
                  <el-option label="启用" value="Y"></el-option>
                  <el-option label="停用" value="N"></el-option>
                </el-select>
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="relRoleOnSearch">查询</el-button>
                <el-button type="info" @click="relRoleOnClean">清空</el-button>
                <el-button type="success" size="mini" @click="relRoleConfirm" v-if="relRoleTableData.length > 0">确定关联</el-button>
              </el-form-item>
            </el-form>
          </el-header>
          <el-main>
            <el-table
              :data="relRoleTableData"
              @selection-change="onRelRoleSelectionChange"
              ref="relRoleMultipleTable"
              :default-sort="{prop: 'last_update_time', order: 'descending'}"
              border max-height="360" style="width: 100%">
              <el-table-column type="selection" width="40"></el-table-column>
              <el-table-column prop="role_name" align="left" label="角色名称" width="150"></el-table-column>
              <el-table-column prop="role_code" align="left" label="角色描述" width="150"></el-table-column>
              <el-table-column prop="valid_status" align="left" label="启用状态" width="100"
                               :formatter="formatterValidStatus"></el-table-column>
              <el-table-column prop="create_time" align="left" :formatter="formatterDate" label="创建日期"
                               width="150"></el-table-column>
              <el-table-column prop="last_update_time" align="left" :formatter="formatterDate" sortable
                               label="最后修改日期"></el-table-column>
            </el-table>
          </el-main>
          <!--<el-footer>-->
            <!--<div class="block">-->
              <!--<el-pagination-->
                <!--@size-change="relRoleSearchFormOnChangePageSize"-->
                <!--@current-change="relRoleSearchFormOnChangeCurrentPage"-->
                <!--:current-page.sync="relRoleSearchForm.paging.current_page"-->
                <!--:page-sizes="[5, 10, 20, 50]"-->
                <!--:page-size="relRoleSearchForm.paging.page_size"-->
                <!--layout="total, sizes, prev, pager, next, jumper"-->
                <!--:total="relRoleSearchFormTotalNum">-->
              <!--</el-pagination>-->
            <!--</div>-->
          <!--</el-footer>-->
        </el-container>
      </el-dialog>
    </el-main>
    <el-footer>
      <div class="block">
        <el-pagination
          @size-change="onChangePageSize"
          @current-change="onChangeCurrentPage"
          :current-page.sync="userSearchForm.paging.current_page"
          :page-sizes="[5, 10, 20, 50]"
          :page-size="userSearchForm.paging.page_size"
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
      onRelGroup(){
        let self = this;
        if (this.userMultipleSelection.length !== 1) {
          self.$message('请选择一项进行操作');
          return false;
        }
        self.relGroupDialogVisible = true;
        //查当前用户所在的用户组数据
        self.$axios.get(
          Constant.ADMIN_PERMISSIONS_USER_GROUPS,
          {
            params: {
              params: {
                user_id: self.userMultipleSelection[0].id
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
      relGroupConfirm(){
        let self = this;
        let allCheck = self.$refs.relGroupRef.getCheckedKeys();
        this.$confirm('确定关联用户组吗?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          self.$axios.post(Constant.ADMIN_PERMISSIONS_USER_GROUPS, {
            params: {
              group_ids: allCheck,
              user_id: self.userMultipleSelection[0].id
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


      ///////////////////////////////     关联角色   /////////////////////
      //确定关联角色
      relRoleConfirm() {
        let self = this;
        let allIds = [];
        for (let index in this.relRoleMultipleSelection) {
          allIds.push(this.relRoleMultipleSelection[index].id);
        }
        self.$axios.post(
          Constant.ADMIN_PERMISSIONS_USER_ROLES,
          {
            params: {
              user_id: self.relRoleCurrentUserId,
              role_ids: allIds
            }
          }
        ).then(function (resp) {
          if (resp.code !== Constant.REQ_SUCCESS) {
            self.$message({type: 'error', message: resp.msg});
            return false;
          }
          self.$message({type: 'success', message: '关联角色成功'});
          self.handleRelRoleDialogClose();
        }).catch(resp => {
          console.log(resp);
          self.$message({type: 'error', message: '系统错误'});
        })
      },
      //点击关联角色
      onRelRole(index, row){
        if (row && row.can_edit === 'N') {
          this.$message({type: 'info', message: row.login_name + '是系统数据不可编辑'});
          return;
        }
        this.relRoleCurrentUserId = row.id;
        this.relRoleDialogVisible = true;
        this.relRoleOnSearch();
      },
      relRoleSearchFormOnChangePageSize(page_size){
        this.relRoleSearchForm.paging.page_size = page_size;
        this.relRoleOnSearch();
      },
      /**
       * 触发修改当前页事件
       */
      relRoleSearchFormOnChangeCurrentPage() {
        this.onSearch();
      },
      //关闭用户组拥有角色列表对话框
      handleRelRoleDialogClose() {
        this.$refs.relRoleMultipleTable.clearSelection();
        this.relRoleDialogVisible = false;
      },
      //清空关联角色查询条件
      relRoleOnClean(){
        this.relRoleSearchForm.role_code = '';
        this.relRoleSearchForm.role_name = '';
        this.relRoleSearchForm.valid_status = '';
      },
      //关联角色搜索
      relRoleOnSearch(){
        let self = this;
        self.$axios.get(Constant.ADMIN_PERMISSIONS_USER_ROLES, {
          params: {
            params: {
              condition: self.relRoleSearchForm,
              user_id: self.relRoleCurrentUserId
            }
          }
        }).then(function (resp) {
          if (resp.code !== Constant.REQ_SUCCESS) {
            self.$message({type: 'error', message: resp.msg});
          } else {
            self.relRoleSearchFormTotalNum = resp.data.total;
            self.relRoleTableData = resp.data.rows;
            //获取当前用户的角色列表
            self.$axios.get(Constant.ADMIN_PERMISSIONS_USER_ROLES_BY_UID,
              {
                params: {
                  user_id: self.relRoleCurrentUserId
                }
              }
            ).then(function (resp) {
              if (resp.code !== Constant.REQ_SUCCESS) {
                self.$message({type: 'error', message: resp.msg});
                self.handleRelRoleDialogClose();
                return false;
              }
              let keys = resp.data;
              if (keys.length > 0) {
                keys.forEach(key => {
                  self.$refs.relRoleMultipleTable.toggleRowSelection(self.relRoleGetRowById(key));
                });
              }
            }).catch(resp => {
              console.log(resp);
              self.$message({type: 'error', message: '系统错误'});
              self.handleRelRoleDialogClose();
            })
          }
        }).catch(function (resp) {
          console.log(resp);
          self.$message({type: 'error', message: '系统错误'});
          self.handleRelRoleDialogClose();
        })
      },
      relRoleGetRowById(id){
        if (id){
          for (let i in this.relRoleTableData){
            if (this.relRoleTableData[i].id === id){
              return this.relRoleTableData[i];
            }
          }
        }
      },
      //关联角色选中数据
      onRelRoleSelectionChange(rows){
        this.relRoleMultipleSelection = rows;
      },
      ///////////////////////////////     关联角色   /////////////////////
      //查询
      onSearch() {
        let self = this;
        this.$axios({
          method: 'get',
          url: Constant.ADMIN_PERMISSIONS_USERS_URI,
          params: {
            params: this.userSearchForm
          }
        }).then(function (resp) {
          if (resp.code !== Constant.REQ_SUCCESS) {
            self.$alert(resp.msg, '系统提示');
          } else {
            self.totalNum = resp.data.total;
            self.userTableData = resp.data.rows;
          }
        }).catch(resp => {
          console.log(resp);
          self.$alert('请求出错', '系统提示');
        });
      },

      //触发删除事件
      onDelete(index, row) {
        let self = this;
        if (!row && this.userMultipleSelection.length < 1) {
          this.$message('请至少选择一项进行操作');
          return;
        } else {
          if (row && row.can_edit === 'N') {
            this.$message({type: 'info', message: row.login_name + '是系统数据不可编辑'});
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
            for (let index in this.userMultipleSelection) {
              deleteIds.push(this.userMultipleSelection[index].id);
            }
          }
          this.$axios.delete(Constant.ADMIN_PERMISSIONS_USERS_URI, {
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
        this.userEditForm.id = '';
        this.userEditForm.login_name = '';
        this.userEditForm.nickname = '';
        this.userEditForm.contact = '';
        this.userEditForm.password = '';
        this.userEditForm.valid_status = 'Y';
      },
      /**
       * 新增、修改
       */
      saveOrUpdate() {
        let self = this;
        this.$refs['userEditForm'].validate((valid) => {
          if (valid) {
            self.$axios.get(Constant.ADMIN_PERMISSIONS_USER_CHECK_UNIQ, {
              params: {
                params: {
                  login_name: self.userEditForm.login_name,
                  rule: {
                    login_name: 'eq'
                  }
                }
              }
            }).then(function (res) {
              if (res.code === Constant.REQ_SUCCESS) {
                if (res.data && res.data.length > 0 && (res.data[0].id !== self.userEditForm.id)) {
                  self.$message({type: 'info', message: '登录名称重复，请重新设置'});
                  return false;
                }
                if (self.userEditForm.id) {
                  self.$axios.post(Constant.ADMIN_PERMISSIONS_USERS_URI, {
                    params: self.userEditForm
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
                  self.$axios.put(Constant.ADMIN_PERMISSIONS_USERS_URI, {
                    params: self.userEditForm
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
              }else {
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
          this.$message({type: 'info', message: row.login_name + '是系统数据不可编辑'});
          return;
        }
        this.userEditForm.id = row.id;
        this.userEditForm.login_name = row.login_name;
        this.userEditForm.nickname = row.nickname;
        this.userEditForm.contact = row.contact;
        this.userEditForm.password = row.password;
        this.userEditForm.valid_status = row.valid_status;
        this.dialogVisible = true;
      },

      /**
       * 触发修改页面条数事件
       */
      onChangePageSize(page_size) {
        this.userSearchForm.paging.page_size = page_size;
        this.onSearch();
      },

      /**
       * 触发修改当前页事件
       */
      onChangeCurrentPage() {
        this.onSearch();
      },

      cleanAllSelect(){
        this.$refs.userMultipleTable.clearSelection();
      },

      /**
       * 清除编辑表单
       */
      onClean() {
        this.userSearchForm.login_name = '';
        this.userSearchForm.nickname = '';
        this.userSearchForm.contact = '';
        this.userSearchForm.valid_status = '';
        this.userSearchForm._s_last_update_time = '';
        this.userSearchForm._e_last_update_time = '';
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
        this.userMultipleSelection = rows;
      },

      //监听选择时间
      listenerSelect(rows){
        if (rows){
          rows.forEach(row => {
            if (row.can_edit === 'N'){
              this.$refs.userMultipleTable.toggleRowSelection(row, false);
            }
          });
        }
      }
    },


    data() {
      let checkAddLoginName = (rule, value, callback) => {
        if (!value) {
          return callback(new Error('请输入登录名称'));
        }
        if (value.length > 20) {
          return callback(new Error('长度不能大于20'));
        }
        if (value.length < 2) {
          return callback(new Error('长度不能小于2'));
        }
        callback();
      };
      let checkAddPassword = (rule, value, callback) => {
        if (value === '') {
          return callback(new Error('请输入密码'));
        }
        if (value.length > 20) {
          return callback(new Error('长度不能大于20'));
        }
        if (value.length < 6) {
          return callback(new Error('长度不能小于6'));
        }
        callback();
      };
      let checkAddNicename = (rule, value, callback) => {
        if (value === '') {
          return callback(new Error('请输入昵称'));
        }
        if (value.length > 20) {
          return callback(new Error('名称长度不能大于20'));
        }
        if (value.length < 2) {
          return callback(new Error('长度不能小于2'));
        }
        callback();
      };
      let checkAddContact = (rule, value, callback) => {
        if (value === '') {
          return callback(new Error('请输入手机号码'));
        }
        let reg = new RegExp("^(13[0-9]|15[012356789]|17[0678]|18[0-9]|14[57])[0-9]{8}$");
        if (!reg.test(value)) {
          return callback(new Error('请输入正确的手机号码'));
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

        ///////////////////////////////     关联角色   /////////////////////
        relRoleDialogVisible: false,
        relRoleMultipleSelection: [],
        relRoleCurrentUserId: '',
        relRoleSearchForm: {
          role_name: '',
          role_code: '',
          valid_status: '',
          group_id: '',
          rule: {
            role_name: 'like',
            role_code: 'like'
          }
        },
        relRoleTableData: [],
        relRoleMultipleTable: [],
        relRoleSearchFormTotalNum: 0,
        ///////////////////////////////     关联角色   /////////////////////

        ///////////////////////////////     编辑用户   /////////////////////
        userEditFormRule: {
          login_name: [
            {validator: checkAddLoginName, trigger: 'blur'}
          ],
          nickname: [
            {validator: checkAddNicename, trigger: 'blur'}
          ],
          contact: [
            {validator: checkAddContact, trigger: 'blur'}
          ],
          password: [
            {validator: checkAddPassword, trigger: 'blur'}
          ]
        },
        dialogVisible: false,
        userEditForm: {
          id: '',
          login_name: '',
          password: '',
          nickname: '',
          contact: '',
          valid_status: 'Y',
        },
        ///////////////////////////////     编辑用户   /////////////////////
        userMultipleSelection: [],
        userSearchForm: {
          login_name: '',
          nickname: '',
          contact: '',
          valid_status: '',
          _s_last_update_time: '',
          _e_last_update_time: '',
          paging: {
            page_size: 5,
            current_page: 1
          },
          rule: {
            login_name: 'like',
            nickname: 'like',
            contact: 'like'
          }
        },
        totalNum: 100,
        userTableData: [],
      }
    },

    /**
     * 计算属性定义
     */
    computed: {

    },

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
