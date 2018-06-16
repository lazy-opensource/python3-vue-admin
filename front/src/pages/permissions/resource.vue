<template>
  <!--资源列表-->
  <el-container>
    <el-header height="30px">
      <el-button type="primary" size="mini" @click="onAdd(0)">新增根资源</el-button>
      <el-button type="primary" size="mini" @click="cleanCheck">全不选</el-button>
      <el-button type="primary" size="mini" @click="resourceAllOpen">展开</el-button>
      <el-button type="primary" size="mini" @click="resourceAllClose">收起</el-button>
      <el-button type="danger" size="mini" @click="onDelete(0)">删除资源</el-button>
    </el-header>
    <el-main>
      <div class="custom-tree-container">
        <div class="block">
          <el-input
            placeholder="输入关键字进行过滤"
            v-model="filterText">
          </el-input>
          <el-tree
            class="filter-tree"
            show-checkbox
            node-key="id"
            :data="resourceData"
            :check-strictly=false
            :props="defaultProps"
            default-expand-all
            :expand-on-click-node="false"
            :filter-node-method="filterNode"
            ref="resourceDataRef">
              <span class="custom-tree-node" slot-scope="{ node, data }">
                <span>{{ node.label }}</span>
                <span>
                  <el-button type="text" size="mini" @click="() => onAdd(node, data)">新增子资源</el-button>
                  <el-button type="text" size="mini" @click="() => onEdit(node, data)">编辑</el-button>
                  <el-button type="text" size="mini" @click="() => onDetails(data)">详情</el-button>
                  <!--<el-button type="text" size="mini" @click="() => onDelete(node, data)">删除资源</el-button>-->
                </span>
            </span>
          </el-tree>
        </div>
      </div>

      <!--新增资源-->
      <el-dialog title="填写资源信息" :visible.sync="dialogVisible" :show-close="false" width="40%">
        <el-form :model="resourceEditForm" status-icon :rules="resourceEditFormRule" ref="resourceEditForm"
                 label-width="100px" class="demo-ruleForm">
          <el-form-item label="资源名称" prop="res_name">
            <el-input type="text" v-model="resourceEditForm.res_name" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="资源描述" prop="res_desc">
            <el-input v-model="resourceEditForm.res_desc"></el-input>
          </el-form-item>
          <el-form-item label="图标" prop="icon">
            <el-input v-model="resourceEditForm.icon"></el-input>
          </el-form-item>
          <el-form-item label="资源编码" prop="res_code">
            <el-input v-model="resourceEditForm.res_code"></el-input>
          </el-form-item>
          <el-form-item label="请求URI" prop="uri">
            <el-input v-model="resourceEditForm.uri"></el-input>
          </el-form-item>
          <el-form-item label="排序" prop="res_order">
            <el-input v-model="resourceEditForm.res_order"></el-input>
          </el-form-item>
          <el-form-item label="资源类型" prop="res_type">
            <el-select v-model="resourceEditForm.res_type" placeholder="资源类型">
              <el-option label="--请选择--" value=""></el-option>
              <el-option label="菜单" value="menu"></el-option>
              <el-option label="后台URL" value="a_uri"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="请求方式" prop="method">
            <el-select v-model="resourceEditForm.method" placeholder="请求方式">
              <el-option label="--请选择--" value=""></el-option>
              <el-option label="GET" value="GET"></el-option>
              <el-option label="POST" value="POST"></el-option>
              <el-option label="PUT" value="PUT"></el-option>
              <el-option label="DELETE" value="DELETE"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="父级资源" prop="res_name">
            <el-input disabled v-model="pname"></el-input>
          </el-form-item>
          <el-form-item label="状态">
            <el-select v-model="resourceEditForm.valid_status" placeholder="状态">
              <el-option label="启用" value="Y"></el-option>
              <el-option label="停用" value="N"></el-option>
            </el-select>
          </el-form-item>
        </el-form>
        <span slot="footer" class="dialog-footer">
          <el-button @click="cancelEdit">取 消</el-button>
          <el-button @click="resetEdit(true)">重 置</el-button>
          <el-button type="primary" @click="saveReource">提 交</el-button>
        </span>
      </el-dialog>

      <!--详情-->
      <el-dialog title="资源详情" :visible.sync="detailsDialogVisible" width="40%"
                 :before-close="handleDetailsDialogClose">
        <el-form status-icon label-width="100px" class="demo-ruleForm">
          <el-form-item label="资源名称:">
            <span>{{resourceDetails.res_name}}</span>
          </el-form-item>
          <el-form-item label="资源描述:">
            <span>{{resourceDetails.res_desc}}</span>
          </el-form-item>
          <el-form-item label="资源URI:">
            <span>{{resourceDetails.uri}}</span>
          </el-form-item>
          <el-form-item label="资源类型:">
            <span v-if="resourceDetails.res_type == 'menu'">菜单</span>
            <span v-if="resourceDetails.res_type == 'a_uri'">后台URL</span>
          </el-form-item>
          <el-form-item label="请求类型:" v-if="resourceDetails.res_type == 'a_uri'">
            <span>{{resourceDetails.method}}</span>
          </el-form-item>
          <el-form-item label="图标:">
            <span>{{resourceDetails.icon}}</span>
          </el-form-item>
          <el-form-item label="排序:">
            <span>{{resourceDetails.res_order}}</span>
          </el-form-item>
          <el-form-item label="创建时间:">
            <span>{{resourceDetails.create_time}}</span>
          </el-form-item>
          <el-form-item label="最后更新时间:">
            <span>{{resourceDetails.last_update_time}}</span>
          </el-form-item>
        </el-form>
      </el-dialog>
    </el-main>
  </el-container>
</template>

<script>
  import * as Constant from "../../constant";
  import Utils from "../../utils";

  export default {
    /**
     * 监听器定义
     * **/
    watch: {
      //资源菜单过滤
      filterText(val) {
        this.$refs.resourceDataRef.filter(val);
      },
      //查看编辑资源过滤
      viewOrEditResFilterText(val) {
        this.$refs.viewOrEditResRef.filter(val);
      }
    },

    /**
     * 计算属性
     * **/
    computed: {
      pname() {
        return this.parent_res_name ? this.parent_res_name : this.default_pname;
      }
    },

    /**
     * 函数定义
     * **/
    methods: {
      //全不选
      cleanCheck() {
        let checkNodeKeys = this.$refs.resourceDataRef.getCheckedKeys();
        for (let i in checkNodeKeys) {
          this.$refs.resourceDataRef.setChecked(checkNodeKeys[i], false, false);
        }
      },
      //展开
      resourceAllOpen() {
        for(var i=0;i<this.$refs.resourceDataRef.store._getAllNodes().length;i++){
          this.$refs.resourceDataRef.store._getAllNodes()[i].expanded= true;
        }
      },
      //收起
      resourceAllClose() {
        for(var i=0;i<this.$refs.resourceDataRef.store._getAllNodes().length;i++){
          this.$refs.resourceDataRef.store._getAllNodes()[i].expanded= false;
        }
      },
      //打开添加资源表单
      onAdd(node, data) {
        if (data.can_edit === 'N'){
          this.$message({type: 'info', message: data.label +  '是系统数据不可编辑'});
          return;
        }
        this.resetEdit(false);
        if (data) {
          this.resourceEditForm.pid = data.id;
          this.parent_res_name = data.label;
          this.dialogVisible = true;
        } else {
          this.resourceEditForm.pid = '' + -1;
          this.parent_resource_name = 'Root';
          this.dialogVisible = true;
        }
      },
      //打开编辑资源表单
      onEdit(node, data) {
        if (data.can_edit === 'N'){
          this.$message({type: 'info', message: data.label +  '是系统数据不可编辑'});
          return;
        }
        let self = this;
        this.resetEdit(false);
        self.$axios.get(Constant.ADMIN_PERMISSIONS_RESOURCES_BY_ID_URI, {
          params: {
            res_id: data.id
          }
        }).then(function (resp) {
          if (resp.code !== Constant.REQ_SUCCESS) {
            self.$message({type: 'error', message: resp.msg});
          } else {
            let data = resp.data;
            self.resourceEditForm.res_desc = data.res_desc;
            self.resourceEditForm.res_name = data.res_name;
            self.resourceEditForm.res_order = data.res_order;
            self.resourceEditForm.uri = data.uri;
            self.resourceEditForm.method = data.method;
            self.resourceEditForm.res_type = data.res_type;
            self.resourceEditForm.icon = data.icon;
            self.resourceEditForm.pid = data.pid;
            self.resourceEditForm.id = data.id;
            self.resourceEditForm.res_code = data.res_code;
            self.dialogVisible = true;
          }
        }).catch(function (resp) {
          console.log(resp);
          self.$message({type: 'error', message: '系统错误'});
        });
      },
      //删除资源
      onDelete(node, data) {
        let checkNodes;
        let self = this;
        if (!node) {
          checkNodes = this.$refs.resourceDataRef.getCheckedNodes();
          if (!checkNodes || checkNodes.length < 1) {
            self.$message({type: 'warning', message: '请至少选择一项进行操作'});
            return;
          }
        }
        this.$confirm('此操作将永久删除数据, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          let deleteIds = [];
          if (node) {
            deleteIds.push(data.id);
            if (data.can_edit === 'N'){
              self.$message({type: 'info', message: data.label +  '是系统数据不可删除'});
              return;
            }
          } else {
            for (let index in checkNodes) {
              if (checkNodes[index].can_edit === 'N'){
                self.$message({type: 'info', message: checkNodes[index].label +  '是系统数据不可删除'});
                return;
              }
              deleteIds.push(checkNodes[index].id);
            }
          }
          this.$axios.delete(Constant.ADMIN_PERMISSIONS_RESOURCES_URI, {
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
      //关闭资源详情对话框
      handleDetailsDialogClose() {
        this.resourceDetails.res_desc = '';
        this.resourceDetails.res_name = '';
        this.resourceDetails.res_code = '';
        this.resourceDetails.method = '';
        this.resourceDetails.icon = '';
        this.resourceDetails.res_order = '';
        this.resourceDetails.res_type = '';
        this.resourceDetails.uri = '';
        this.resourceDetails.create_time = '';
        this.resourceDetails.last_update_time = '';
        this.detailsDialogVisible = false;
      },

      //资源详情
      onDetails(data) {
        this.handleDetailsDialogClose();
        let self = this;
        let res_id = data.id;
        self.$axios.get(Constant.ADMIN_PERMISSIONS_RESOURCES_BY_ID_URI, {
          params: {
            res_id: res_id
          }
        }).then(function (resp) {
          if (resp.code !== Constant.REQ_SUCCESS) {
            self.$message({type: 'error', message: resp.msg});
          } else {
            let data = resp.data;
            self.resourceDetails.res_desc = data.res_desc;
            self.resourceDetails.res_name = data.res_name;
            self.resourceDetails.res_order = data.res_order;
            self.resourceDetails.uri = data.uri;
            self.resourceDetails.method = data.method;
            self.resourceDetails.create_time = self.formatterDate(data.create_time);
            self.resourceDetails.last_update_time = self.formatterDate(data.last_update_time);
            self.resourceDetails.res_type = data.res_type;
            self.resourceDetails.icon = data.icon;
            self.resourceDetails.res_code = data.res_code;
            self.detailsDialogVisible = true;
          }
        }).catch(function (resp) {
          console.log(resp);
          self.$message({type: 'error', message: '系统错误'});
        });
      },

      //资源查询
      onSearch() {
        let self = this;
        this.$axios({
          method: 'get',
          url: Constant.ADMIN_PERMISSIONS_RESOURCES_URI
        }).then(function (resp) {
          if (resp.code !== Constant.REQ_SUCCESS) {
            self.$alert(resp.msg, '系统提示');
          } else {
            self.resourceData = resp.data.rows;
          }
          self.loading = false;
        }).catch(resp => {
          console.log(resp);
          self.$alert('请求出错', '系统提示');
          self.loading = false;
        });
      },
      //添加资源
      saveReource() {
        let self = this;
        this.$refs['resourceEditForm'].validate((valid) => {
          if (valid) {
            self.$axios.get(Constant.ADMIN_PERMISSIONS_RESOURCE_CHECK_UNIQ, {
              params: {
                params: {
                  res_name: self.resourceEditForm.res_name,
                  rule: {
                    res_name: 'eq'
                  }
                }
              }
            }).then(function (res) {
              if (res.code === Constant.REQ_SUCCESS){
                if (res.data && res.data.length > 0 && (res.data[0].id !== self.resourceEditForm.id)){
                  self.$message({type: 'error', message: '资源名称重复，请重新设置'});
                  return false;
                }
                self.$axios.get(Constant.ADMIN_PERMISSIONS_RESOURCE_CHECK_UNIQ, {
                  params: {
                    params: {
                      res_code: self.resourceEditForm.res_code,
                      rule: {
                        res_code: 'eq'
                      }
                    }
                  }
                }).then(function (res) {
                  if (res.code === Constant.REQ_SUCCESS){
                    if (res.data && res.data.length > 0 && (res.data[0].id !== self.resourceEditForm.id)){
                      self.$message({type: 'error', message: '资源编码重复，请重新设置'});
                      return false;
                    }
                    //修改
                    if (self.resourceEditForm.id){
                      self.$axios.post(Constant.ADMIN_PERMISSIONS_RESOURCES_URI, {
                        params: self.resourceEditForm
                      }).then(function (resp) {
                        if (resp.code === Constant.REQ_SUCCESS) {
                          self.onSearch();
                          self.$message({type: 'success', message: '添加成功!'});
                        } else {
                          self.$message({type: 'info', message: resp.msg});
                        }
                      }).catch(resp => {
                        console.log(resp);
                        self.$message({type: 'error', message: '系统错误'});
                      });
                    }else {
                      //新增
                      self.$axios.put(Constant.ADMIN_PERMISSIONS_RESOURCES_URI, {
                        params: self.resourceEditForm
                      }).then(function (resp) {
                        if (resp.code === Constant.REQ_SUCCESS) {
                          self.onSearch();
                          self.$message({type: 'success', message: '添加成功!'});
                        } else {
                          self.$message({type: 'info', message: resp.msg});
                        }
                      }).catch(resp => {
                        console.log(resp);
                        self.$message({type: 'error', message: '系统错误'});
                      });
                    }
                    self.dialogVisible = false;
                  }else {
                    console.log(res);
                    self.$message({type: 'error', message: '系统错误'});
                  }
                }).catch(resp => {
                  console.log(resp);
                  self.$message({type: 'error', message: '系统错误'});
                });
              }else {
                console.log(res);
                self.$message({type: 'error', message: '系统错误'});
              }
            }).catch(resp => {
              console.log(resp);
              self.$message({type: 'error', message: '系统错误'});
            });
          } else {
            this.$message({type: 'warning', message: '表单验证不通过'});
          }
        });
      },
      //取消编辑
      cancelEdit() {
        this.resetEdit(false);
        this.dialogVisible = false;
      },

      //重置添加资源表单信息按钮
      resetEdit(form) {
        this.resourceEditForm.res_desc = '';
        this.resourceEditForm.res_name = '';
        this.resourceEditForm.res_code = '';
        this.resourceEditForm.method = '';
        this.resourceEditForm.icon = 'el-icon-menu';
        this.resourceEditForm.res_order = '100';
        if (!form){
          this.resourceEditForm.pid = '';
          this.resourceEditForm.id = '';
        }
        this.resourceEditForm.res_type = '';
        this.resourceEditForm.valid_status = 'Y';
        this.resourceEditForm.uri = '';
      },

      //过滤资源
      filterNode(value, data) {
        if (!value) return true;
        return data.label.indexOf(value) !== -1;
      },
      //格式化启用状态
      formatterValidStatus(row, column, cellValue) {
        if (cellValue === 'Y') {
          return '启用'
        } else {
          return '停用'
        }
      },
      //格式化日期格式
      formatterDate(value) {
        return Utils.formatDate(new Date(value), 'yyyy-MM-dd')
      },
    },


    /**
     * 属性定义
     * */
    data() {
      // 添加/列表资源相关
      let checkAddResourceName = (rule, value, callback) => {
        if (!value) {
          return callback(new Error('请输入资源名称'));
        }
        if (value.length > 30) {
          return callback(new Error('长度不能大于30'));
        }
        callback();
      };
      let checkAddResourceDesc = (rule, value, callback) => {
        if (value === '') {
          return callback(new Error('请输入资源描述信息'));
        }
        if (('' + value) > 40) {
          return callback(new Error('长度不能大于40'));
        }
        callback();
      };
      let checkAddResourceCode = (rule, value, callback) => {
        if (value === '') {
          return callback(new Error('请输入资源编码'));
        }
        if (('' + value) > 40) {
          return callback(new Error('长度不能大于40'));
        }
        callback();
      };
      let checkAddResourceType = (rule, value, callback) => {
        if (value === '') {
          return callback(new Error('请输入资源类型'));
        }
        if (('' + value) > 10) {
          return callback(new Error('长度不能大于10'));
        }
        callback();
      };
      let checkAddResourceMethod = (rule, value, callback) => {
        if (this.resourceEditForm.res_type === 'a_uri'){
          if (value === '') {
            return callback(new Error('请输入请求方式'));
          }
          if (('' + value) > 40) {
            return callback(new Error('长度不能大于40'));
          }
        }
        callback();
      };
      let checkAddResourceUri = (rule, value, callback) => {
        if (this.resourceEditForm.res_type === 'a_uri'){
          if (value === '') {
            return callback(new Error('请输入请求URI'));
          }
          if (('' + value) > 40) {
            return callback(new Error('长度不能大于40'));
          }
        }
        callback();
      };
      return {
        detailsDialogVisible: false,
        dialogVisible: false,
        resourceDetails: {
          res_desc: '',
          res_code: '',
          res_name: '',
          pid: '',
          uri: '',
          res_type: '',
          res_order: '',
          method: '',
          icon: '',
          valid_status: 'Y',
          create_time: '',
          last_update_time: ''
        },
        resourceEditForm: {
          id: '',
          res_desc: '',
          res_code: '',
          res_name: '',
          pid: '',
          uri: '',
          res_type: '',
          res_order: '100',
          method: '',
          icon: 'el-icon-menu',
          valid_status: 'Y'
        },
        // 资源-添加/列表/详情相关
        resourceEditFormRule: {
          res_name: [
            {validator: checkAddResourceName, trigger: 'blur'}
          ],
          res_desc: [
            {validator: checkAddResourceDesc, trigger: 'blur'}
          ],
          res_code: [
            {validator: checkAddResourceCode, trigger: 'blur'}
          ],
          res_type: [
            {validator: checkAddResourceType, trigger: 'blur'}
          ],
          method: [
            {validator: checkAddResourceMethod, trigger: 'blur'}
          ],
          uri: [
            {validator: checkAddResourceUri, trigger: 'blur'}
          ]
        },
        parent_res_name: '',
        default_pname: '顶级资源',
        filterText: '',
        resourceData: [],
        defaultProps: {
          children: 'children',
          label: 'label'
        },
        loading: true,
      }
    },
    mounted: function () {
      this.onSearch();
    },
    /**
     * 初始化钩子函数
     */
    created: function () {
      // this.onSearch();
      // this.initViewOrEditResData();
    }
  };
</script>

<style scoped>

  .el-header {
    background-color: #E9EEF3;
    color: #333;
    text-align: left;
    margin: 0px;
    line-height: 0px;
  }

  .custom-tree-node {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 14px;
    padding-right: 8px;
  }

  .el-main {
    background-color: #E9EEF3;
    color: #333;
    text-align: center;
    line-height: 0px;
    overflow-y: auto;
    height: calc(100vh - 130px);
  }

  body > .el-container {
    margin-bottom: 40px;
  }

  .el-container:nth-child(5) .el-aside,
  .el-container:nth-child(6) .el-aside {
    line-height: 260px;
  }

  .el-container:nth-child(7) .el-aside {
    line-height: 320px;
  }
</style>
