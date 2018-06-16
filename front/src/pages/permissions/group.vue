<template>
  <!--用户组列表-->
    <el-container>
      <el-header height="30px">
        <el-button type="primary" size="mini" @click="onAdd(0)">新增根用户组</el-button>
        <el-button type="primary" size="mini" @click="cleanCheck">全不选</el-button>
        <el-button type="primary" size="mini" @click="groupAllOpen">展开</el-button>
        <el-button type="primary" size="mini" @click="groupAllClose">收起</el-button>
        <el-button type="danger" size="mini" @click="onDelete(0)">删除用户组</el-button>
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
              :data="groupData"
              :check-strictly=false
              :props="defaultProps"
              default-expand-all
              :expand-on-click-node="false"
              :filter-node-method="filterNode"
              ref="groupDataRef">
              <span class="custom-tree-node" slot-scope="{ node, data }">
                <span>{{ node.label }}</span>
                <span>
                  <el-button type="text" size="mini" @click="() => editResource(data)">查看/编辑权限</el-button>
                  <el-button type="text" size="mini" @click="() => clickEdit(data)">编辑</el-button>
                  <el-button type="text" size="mini" @click="() => hasRoles(data)">角色列表</el-button>
                  <el-button type="text" size="mini" @click="() => hasUsers(data)">用户列表</el-button>
                  <el-button type="text" size="mini" @click="() => onAdd(node, data)">新增子用户组</el-button>
                  <el-button type="text" size="mini" @click="() => onDetails(data)">详情</el-button>
                  <!--<el-button type="text" size="mini" @click="() => onDelete(node, data)">删除用户组</el-button>-->
                </span>
            </span>
            </el-tree>
          </div>
        </div>

        <!--新增用户组-->
        <el-dialog title="填写用户组信息" :visible.sync="dialogVisible" :show-close="false" width="40%">
          <el-form :model="groupAddForm" status-icon :rules="groupAddFormRule" ref="groupAddForm"
                   label-width="100px" class="demo-ruleForm">
            <el-form-item label="用户组名称" prop="group_name">
              <el-input type="text" v-model="groupAddForm.group_name" auto-complete="off"></el-input>
            </el-form-item>
            <el-form-item label="用户组描述" prop="group_desc">
              <el-input v-model="groupAddForm.group_desc"></el-input>
            </el-form-item>
            <el-form-item label="用户组编码" prop="group_code">
              <el-input v-model="groupAddForm.group_code"></el-input>
            </el-form-item>
            <el-form-item label="父级用户组" prop="group_name">
              <el-input disabled v-model="pname"></el-input>
            </el-form-item>
            <el-form-item label="状态">
              <el-select v-model="groupAddForm.valid_status" placeholder="状态">
                <el-option label="启用" value="Y"></el-option>
                <el-option label="停用" value="N"></el-option>
              </el-select>
            </el-form-item>
          </el-form>
          <span slot="footer" class="dialog-footer">
          <el-button @click="cancelAdd">取 消</el-button>
          <el-button @click="resetAdd">重 置</el-button>
          <el-button type="primary" @click="saveGroup">创 建</el-button>
        </span>
        </el-dialog>

        <!--详情-->
        <el-dialog title="用户组详情" :visible.sync="detailsDialogVisible" width="40%"
                   :before-close="handleDetailsDialogClose">
          <el-form status-icon label-width="100px" class="demo-ruleForm">
            <el-form-item label="用户组名称:">
              <span>{{groupDetails.group_name}}</span>
            </el-form-item>
            <el-form-item label="用户组编码:">
              <span>{{groupDetails.group_code}}</span>
            </el-form-item>
            <el-form-item label="用户组描述:">
              <span>{{groupDetails.group_desc}}</span>
            </el-form-item>
          </el-form>
        </el-dialog>

        <!--用户列表-->
        <el-dialog title="该组拥有的用户" :visible.sync="usersDialogVisible" width="70%"
                   :before-close="handleUsersDialogClose">
          <el-container>
            <el-header height="50">
              <el-form :inline="true" :model="usersSearchForm" size="mini" class="demo-form-inline">
                <el-form-item label="登录账号">
                  <el-input v-model="usersSearchForm.login_name" placeholder="登录账号"></el-input>
                </el-form-item>
                <el-form-item label="昵称">
                  <el-input v-model="usersSearchForm.nickname" placeholder="昵称"></el-input>
                </el-form-item>
                <el-form-item label="联系方式">
                  <el-input v-model="usersSearchForm.contact" placeholder="联系方式"></el-input>
                </el-form-item>
                <el-form-item label="启用状态">
                  <el-select v-model="usersSearchForm.valid_status" placeholder="启用状态">
                    <el-option label="--请选择--" value=""></el-option>
                    <el-option label="启用" value="Y"></el-option>
                    <el-option label="停用" value="N"></el-option>
                  </el-select>
                </el-form-item>
                <el-form-item>
                  <el-button type="primary" @click="usersOnSearch">查询</el-button>
                  <el-button type="primary" @click="usersOnClean">清空</el-button>
                </el-form-item>
              </el-form>
            </el-header>
            <el-main>
              <el-table
                :data="usersTableData"
                ref="usersMultipleTable"
                :default-sort="{prop: 'last_update_time', order: 'descending'}"
                border max-height="360" style="width: 100%">
                <el-table-column prop="login_name" align="left" label="登录账号" width="150"></el-table-column>
                <el-table-column prop="nickname" align="left" label="昵称" width="150"></el-table-column>
                <el-table-column prop="contact" align="left" label="联系方式" width="150"></el-table-column>
                <el-table-column prop="valid_status" align="left" label="启用状态" width="100"
                                 :formatter="formatterValidStatus"></el-table-column>
                <el-table-column prop="create_time" align="left" :formatter="formatterDate" label="创建日期"
                                 width="150"></el-table-column>
                <el-table-column prop="last_update_time" align="left" :formatter="formatterDate" sortable
                                 label="最后修改日期"></el-table-column>
              </el-table>
            </el-main>
            <el-footer>
              <div class="block">
                <el-pagination
                  @size-change="usersSearchFormOnChangePageSize"
                  @current-change="usersSearchFormOnChangeCurrentPage"
                  :current-page.sync="usersSearchForm.paging.current_page"
                  :page-sizes="[5, 10, 20, 50]"
                  :page-size="usersSearchForm.paging.page_size"
                  layout="total, sizes, prev, pager, next, jumper"
                  :total="usersSearchFormTotalNum">
                </el-pagination>
              </div>
            </el-footer>
          </el-container>
        </el-dialog>

        <!--角色列表-->
        <el-dialog title="该组拥有的角色" :visible.sync="rolesDialogVisible" width="60%"
                   :before-close="handleRolesDialogClose">
          <el-container>
            <el-header height="50">
              <el-form :inline="true" :model="rolesSearchForm" size="mini" class="demo-form-inline">
                <el-form-item label="角色名称">
                  <el-input v-model="rolesSearchForm.role_name" placeholder="角色名称"></el-input>
                </el-form-item>
                <el-form-item label="角色编码">
                  <el-input v-model="rolesSearchForm.role_code" placeholder="角色编码"></el-input>
                </el-form-item>
                <el-form-item label="启用状态">
                  <el-select v-model="rolesSearchForm.valid_status" placeholder="启用状态">
                    <el-option label="--请选择--" value=""></el-option>
                    <el-option label="启用" value="Y"></el-option>
                    <el-option label="停用" value="N"></el-option>
                  </el-select>
                </el-form-item>
                <el-form-item>
                  <el-button type="primary" @click="rolesOnSearch">查询</el-button>
                  <el-button type="info" @click="rolesOnClean">清空</el-button>
                </el-form-item>
              </el-form>
            </el-header>
            <el-main>
              <el-table
                :data="rolesTableData"
                ref="rolesMultipleTable"
                :default-sort="{prop: 'last_update_time', order: 'descending'}"
                border max-height="360" style="width: 100%">
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
            <el-footer>
              <div class="block">
                <el-pagination
                  @size-change="rolesSearchFormOnChangePageSize"
                  @current-change="rolesSearchFormOnChangeCurrentPage"
                  :current-page.sync="rolesSearchForm.paging.current_page"
                  :page-sizes="[5, 10, 20, 50]"
                  :page-size="rolesSearchForm.paging.page_size"
                  layout="total, sizes, prev, pager, next, jumper"
                  :total="rolesSearchFormTotalNum">
                </el-pagination>
              </div>
            </el-footer>
          </el-container>
        </el-dialog>

        <!--查看/编辑资源权限-->
        <el-dialog title="查看/编辑资源权限" :visible.sync="viewOrEditResDialogVisible" width="80%"
                   :before-close="handleViewOrEditResDialogClose">
          <el-container>
            <el-main>
              <div class="custom-tree-container">
                <div class="block">
                  <el-input
                    placeholder="输入关键字进行过滤"
                    v-model="viewOrEditResFilterText">
                  </el-input>
                  <el-tree
                    class="filter-tree"
                    show-checkbox
                    check-strictly
                    node-key="id"
                    :expand-on-click-node="false"
                    :data="viewOrEditResData"
                    :props="viewOrEditResDefaultProps"
                    default-expand-all
                    :filter-node-method="viewOrEditResFilterNode"
                    ref="viewOrEditResRef">
              <span class="custom-tree-node" slot-scope="{ node, data }">
                <span>{{ node.label }}</span>
                <span>
                  <el-button type="text" size="mini" @click="() => viewOrEditResOnDetails(data)">详情</el-button>
                  <el-button type="text" size="mini"
                             @click="() => viewOrEditResOnDelete(node, data)">删除资源关联关系</el-button>
                </span>
            </span>
                  </el-tree>
                </div>
              </div>
            </el-main>
            <el-footer height="50" style="margin-top: 10px;">
              <el-button type="primary" size="mini" @click="viewOrEditResReset">分配资源</el-button>
            </el-footer>
          </el-container>
        </el-dialog>

        <!--用户组编辑资源资源详情-->
        <el-dialog title="资源详情" :visible.sync="viewOrEditResDetailsVisible" width="40%"
                   :before-close="handleViewOrEditResDetailDialogClose">
          <el-form status-icon label-width="100px" class="demo-ruleForm">
            <el-form-item label="资源名称:">
              <span>{{viewOrEditResDetailsPopoverObj.res_name}}</span>
            </el-form-item>
            <el-form-item label="资源描述:">
              <span>{{viewOrEditResDetailsPopoverObj.res_desc}}</span>
            </el-form-item>
            <el-form-item label="资源URI:">
              <span>{{viewOrEditResDetailsPopoverObj.res_uri}}</span>
            </el-form-item>
            <el-form-item label="资源类型:">
              <span v-if="viewOrEditResDetailsPopoverObj.res_type == 'menu'">菜单</span>
              <span v-if="viewOrEditResDetailsPopoverObj.res_type == 'a_uri'">后台URL</span>
            </el-form-item>
            <el-form-item label="请求类型:" v-if="viewOrEditResDetailsPopoverObj.res_type == 'a_uri'">
              <span>{{viewOrEditResDetailsPopoverObj.method}}</span>
            </el-form-item>
          </el-form>
        </el-dialog>

        <!--修改用户组信息-->
        <el-dialog title="修改用户组信息" :visible.sync="editGroupDialogVisible" :show-close="false" width="40%">
          <el-form :model="groupEditForm" status-icon :rules="groupEditFormRule" ref="groupEditForm"
                   label-width="100px" class="demo-ruleForm">
            <el-form-item label="用户组名称" prop="group_name">
              <el-input type="text" v-model="groupEditForm.group_name" auto-complete="off"></el-input>
            </el-form-item>
            <el-form-item label="用户组描述" prop="group_desc">
              <el-input type="text" v-model="groupEditForm.group_desc" auto-complete="off"></el-input>
            </el-form-item>
          </el-form>
          <span slot="footer" class="dialog-footer">
          <el-button @click="cancelEdit">取 消</el-button>
          <el-button @click="resetEdit">重 置</el-button>
          <el-button type="primary" @click="editGroup">修 改</el-button>
        </span>
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
      //用户组菜单过滤
      filterText(val) {
        this.$refs.groupDataRef.filter(val);
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
        return this.parent_group_name ? this.parent_group_name : this.default_pname;
      }
    },

    /**
     * 函数定义
     * **/
    methods: {
      //用户组拥有用户列表
      hasUsers(data) {
        this.usersSearchForm.group_id = data.id;
        this.usersOnSearch('hasUsers');
      },
      //关闭用户组拥有用户列表对话框
      handleUsersDialogClose() {
        this.usersOnClean();
        this.usersDialogVisible = false;
      },
      // 检索用户列表
      usersOnSearch(call_from) {
        let self = this;
        self.$axios.get(Constant.ADMIN_PERMISSIONS_GROUP_USERS_URI, {
          params: {
            params: this.usersSearchForm
          }
        }).then(function (resp) {
          if (resp.code !== Constant.REQ_SUCCESS) {
            self.$message({type: 'error', message: resp.msg});
          } else {
            self.usersSearchFormTotalNum = resp.data.total;
            if (call_from === 'hasUsers' && self.usersSearchFormTotalNum < 1) {
              self.$alert("该用户组没有用户相关信息", '系统提示');
            } else {
              self.usersTableData = resp.data.rows;
              self.usersDialogVisible = true;
            }
          }
        }).catch(function (resp) {
          console.log(resp);
          self.$message({type: 'error', message: '系统错误'});
        })
      },
      // 清空用户列表检索条件
      usersOnClean() {
        this.usersSearchForm.login_name = '';
        this.usersSearchForm.nickname = '';
        this.usersSearchForm.valid_status = '';
        this.usersSearchForm.contact = '';
      },
      //用户列表页面大小改变回调
      usersSearchFormOnChangePageSize(page_size) {
        this.usersSearchForm.paging.page_size = page_size;
        this.usersOnSearch();
      },
      //用户列表当前页改变回调
      usersSearchFormOnChangeCurrentPage() {
        this.usersOnSearch();
      },
      //用户组拥有角色列表
      hasRoles(data) {
        this.rolesSearchForm.group_id = data.id;
        this.rolesOnSearch('hasRoles');
      },
      //关闭用户组拥有角色列表对话框
      handleRolesDialogClose() {
        this.rolesOnClean();
        this.rolesDialogVisible = false;
      },
      // 检索角色列表
      rolesOnSearch(call_from) {
        let self = this;
        self.$axios.get(Constant.ADMIN_PERMISSIONS_GROUP_ROLES_URI, {
          params: {
            params: this.rolesSearchForm
          }
        }).then(function (resp) {
          if (resp.code !== Constant.REQ_SUCCESS) {
            self.$message({type: 'error', message: resp.msg});
          } else {
            self.rolesSearchFormTotalNum = resp.data.total;
            if (call_from === 'hasRoles' && self.rolesSearchFormTotalNum < 1) {
              self.$alert("该用户组没有角色相关信息", '系统提示');
            } else {
              self.rolesTableData = resp.data.rows;
              self.rolesDialogVisible = true;
            }
          }
        }).catch(function (resp) {
          console.log(resp);
          self.$message({type: 'error', message: '系统错误'});
        })
      },
      // 清空角色列表检索条件
      rolesOnClean() {
        this.rolesSearchForm.role_code = '';
        this.rolesSearchForm.role_name = '';
        this.rolesSearchForm.valid_status = '';
      },
      //用户列表页面大小改变回调
      rolesSearchFormOnChangePageSize(page_size) {
        this.rolesSearchForm.paging.page_size = page_size;
        this.rolesOnSearch();
      },
      //用户列表当前页改变回调
      rolesSearchFormOnChangeCurrentPage() {
        this.rolesOnSearch();
      },
      //查看/编辑资源权限关闭对话框回调
      handleViewOrEditResDialogClose() {
        this.$refs.viewOrEditResRef.setCheckedKeys([]);
        this.viewOrEditResDialogVisible = false;
      },
      //查看编辑资源
      editResource(data) {
        let self = this;
        self.viewOrEditResDialogVisible = true;
        self.current_check_group = data.name;
        self.edit_resource_group_id = data.id;
        self.viewOrEditOnSearch(data.id);
      },
      clickEdit(data){
        this.editGroupDialogVisible = true;
        this.groupEditForm.group_name = data.label;
        this.groupEditForm.group_desc = data.desc;
        this.groupEditForm.id = data.id;
      },
      //查看/编辑资源检索
      viewOrEditOnSearch(id) {
        let self = this;
        self.$axios.get(Constant.ADMIN_PERMISSIONS_GROUP_RESOURCES_BY_GID_URI, {
          params: {
            params: {
              group_id: id
            }
          }
        }).then(function (res) {
          if (res.code !== Constant.REQ_SUCCESS) {
            self.$message({type: 'error', message: res.msg});
          } else {
            let current_resources = res.data.rows;
            let keys = [];
            for (let i in current_resources) {
              keys.push(current_resources[i].id);
            }
            self.$refs.viewOrEditResRef.setCheckedKeys(keys, false);
          }
        }).catch(function (res) {
          console.log(res);
          self.$message({type: 'error', message: '系统错误'});
        })
      },

      //删除资源
      viewOrEditResOnDelete(node, data){
        let res_id = data.id;
        let self = this;
        if (data.can_edit == 'N'){
          self.$message({type: 'info', message:  '系统数据不可删除'});
          return;
        }
        self.$axios.delete(Constant.ADMIN_PERMISSIONS_GROUP_RESOURCES_URI, {
          params: {
            params: {
              rid: res_id,
              gid: self.edit_resource_group_id,
              rule: {
                rid: 'eq',
                gid: 'eq'
              }
            }
          }
        }).then(function (resp) {
          if (resp.code !== Constant.REQ_SUCCESS) {
            self.$message({type: 'error', message: res.msg});
          } else {
            self.$message({type: 'success', message: '删除成功'});
            self.viewOrEditResDialogVisible = false;
          }
        }).catch(function (res) {
          console.log(res);
          self.$message({type: 'success', message: '系统错误'});
        })
      },
      //初始化查看编辑资源对话框树
      initViewOrEditResData() {
        let self = this;
        self.$axios.get(Constant.ADMIN_PERMISSIONS_GROUP_RESOURCES_URI).then(function (res) {
          if (res.code !== Constant.REQ_SUCCESS) {
            self.$message({type: 'error', message: res.msg});
          } else {
            self.viewOrEditResData = res.data.rows;
          }
        }).catch(function (res) {
          console.log(res);
          self.$message({type: 'error', message: '系统错误'});
        })
      },
      //编辑资源资源详情
      viewOrEditResOnDetails(data) {
        let self = this;
        self.viewOrEditResDetailsPopoverObjClean();
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
            self.viewOrEditResDetailsPopoverObj.res_desc = data.res_desc;
            self.viewOrEditResDetailsPopoverObj.res_name = data.res_name;
            self.viewOrEditResDetailsPopoverObj.res_uri = data.uri;
            self.viewOrEditResDetailsPopoverObj.res_type = data.res_type;
            self.viewOrEditResDetailsPopoverObj.res_code = data.res_code;
            self.viewOrEditResDetailsVisible = true;
          }
        }).catch(function (resp) {
          console.log(resp);
          self.$message({type: 'error', message: '系统错误'});
        })
      },
      //清除资源详情对象数据
      viewOrEditResDetailsPopoverObjClean(){
        this.viewOrEditResDetailsPopoverObj.method = '';
        this.viewOrEditResDetailsPopoverObj.res_desc = '';
        this.viewOrEditResDetailsPopoverObj.res_name = '';
        this.viewOrEditResDetailsPopoverObj.res_type = '';
        this.viewOrEditResDetailsPopoverObj.res_uri = '';
        this.viewOrEditResDetailsPopoverObj.res_code = "";
      },
      //查看/编辑资源重新分配回调
      viewOrEditResReset() {
        let self = this;
        let allCheck = self.$refs.viewOrEditResRef.getCheckedKeys();
        let halfCheck = self.$refs.viewOrEditResRef.getHalfCheckedKeys();
        if (allCheck && halfCheck) {
          allCheck = allCheck.concat(halfCheck);
        } else if (halfCheck) {
          allCheck = halfCheck;
        }
        this.$confirm('确定重新分配资源吗?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          self.$axios.post(Constant.ADMIN_PERMISSIONS_GROUP_RESOURCES_URI, {
            params: {
              params: {
                group_id: self.edit_resource_group_id,
                res_ids: allCheck
              }
            }
          }).then(function (resp) {
            if (resp.code === Constant.REQ_SUCCESS) {
              // self.viewOrEditOnSearch(self.edit_resource_group_id, self);
              self.$message({type: 'success', message: '分配资源成功!'});
              self.handleViewOrEditResDialogClose();
            } else {
              self.$message({type: 'error', message: resp.msg});
            }
          }).catch(resp => {
            self.$message({type: 'error', message: '服务器错误'});
          });
        }).catch(() => {
          self.$message({type: 'info', message: '已取消'});
        });
      },
      //过滤用户组关联资源
      viewOrEditResFilterNode(value, data) {
        if (!value) return true;
        return data.label.indexOf(value) !== -1;
      },
      //全不选
      cleanCheck() {
        let checkNodeKeys = this.$refs.groupDataRef.getCheckedKeys();
        for (let i in checkNodeKeys) {
          this.$refs.groupDataRef.setChecked(checkNodeKeys[i], false, false);
        }
      },
      //展开
      groupAllOpen() {
        for(var i=0;i<this.$refs.groupDataRef.store._getAllNodes().length;i++){
          this.$refs.groupDataRef.store._getAllNodes()[i].expanded= true;
        }
      },
      //收起
      groupAllClose() {
        for(var i=0;i<this.$refs.groupDataRef.store._getAllNodes().length;i++){
          this.$refs.groupDataRef.store._getAllNodes()[i].expanded= false;
        }
      },
      //打开添加用户组表单
      onAdd(node, data) {
        this.resetAdd();
        if (data) {
          this.groupAddForm.pid = data.id;
          this.parent_group_name = data.label;
          this.dialogVisible = true;
        } else {
          this.groupAddForm.pid = '' + -1;
          this.parent_group_name = 'Root';
          this.dialogVisible = true;
        }
      },
      //删除用户组
      onDelete(node, data) {
        let checkNodes;
        let self = this;
        if (!node) {
          checkNodes = self.$refs.groupDataRef.getCheckedNodes();
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
          this.$axios.delete(Constant.ADMIN_PERMISSIONS_GROUPS_URI, {
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
      //关闭用户组详情对话框
      handleDetailsDialogClose() {
        this.groupDetails.group_desc = '';
        this.groupDetails.group_name = '';
        this.groupDetails.group_code = '';
        this.detailsDialogVisible = false;
      },
      //关闭查看和编辑资源资源详情对话框
      handleViewOrEditResDetailDialogClose() {
        this.viewOrEditResDetailsPopoverObjClean();
        this.viewOrEditResDetailsVisible = false;
      },
      //用户组详情
      onDetails(data) {
        this.handleDetailsDialogClose();
        this.groupDetails.group_name = data.label;
        this.groupDetails.group_desc = data.desc;
        this.groupDetails.group_code = data.code;
        this.detailsDialogVisible = true;
      },

      //用户组查询
      onSearch() {
        let self = this;
        this.$axios({
          method: 'get',
          url: Constant.ADMIN_PERMISSIONS_GROUPS_URI
        }).then(function (resp) {
          if (resp.code !== Constant.REQ_SUCCESS) {
            self.$alert(resp.msg, '系统提示');
          } else {
            self.groupData = resp.data.rows;
          }
          self.loading = false;
        }).catch(resp => {
          console.log(resp);
          self.$alert('请求出错', '系统提示');
          self.loading = false;
        });
      },
      //编辑用户组
      editGroup(){
        let self = this;
        this.$refs['groupEditForm'].validate((valid) => {
          if (valid) {
            self.$axios.get(Constant.ADMIN_PERMISSIONS_GROUP_CHECK_UNIQ, {
              params: {
                params: {
                  group_name: self.groupEditForm.group_name,
                  rule: {
                    group_name: 'eq'
                  }
                }
              }
            }).then(function (res) {
              if (res.code === Constant.REQ_SUCCESS){
                if (res.data && res.data.length > 0 && (res.data[0].id !== self.groupEditForm.id)){
                  self.$message({type: 'error', message: '用户组名称重复，请重新设置'});
                  return false;
                }
                self.$axios.post(Constant.ADMIN_PERMISSIONS_GROUPS_URI, {
                  params: self.groupEditForm
                }).then(function (resp) {
                  if (resp.code === Constant.REQ_SUCCESS) {
                    self.onSearch();
                    self.$message({type: 'success', message: '编辑成功!'});
                  } else {
                    self.$message({type: 'info', message: resp.msg});
                  }
                }).catch(resp => {
                  console.log(resp);
                  self.$message({type: 'error', message: '系统错误'});
                });
                self.editGroupDialogVisible = false;
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
      //添加用户组
      saveGroup() {
        let self = this;
        this.$refs['groupAddForm'].validate((valid) => {
          if (valid) {
            self.$axios.get(Constant.ADMIN_PERMISSIONS_GROUP_CHECK_UNIQ, {
              params: {
                params: {
                  group_name: self.groupAddForm.group_name,
                  rule: {
                    group_name: 'eq'
                  }
                }
              }
            }).then(function (res) {
              if (res.code === Constant.REQ_SUCCESS){
                if (res.data && res.data.length > 0){
                  self.$message({type: 'error', message: '用户组名称重复，请重新设置'});
                  return false;
                }
                self.$axios.get(Constant.ADMIN_PERMISSIONS_GROUP_CHECK_UNIQ, {
                  params: {
                    params: {
                      group_code: self.groupAddForm.group_code,
                      rule: {
                        group_code: 'eq'
                      }
                    }
                  }
                }).then(function (res) {
                  if (res.code === Constant.REQ_SUCCESS){
                    if (res.data && res.data.length > 0){
                      self.$message({type: 'error', message: '用户组编码重复，请重新设置'});
                      return false;
                    }

                    self.$axios.put(Constant.ADMIN_PERMISSIONS_GROUPS_URI, {
                      params: self.groupAddForm
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
      cancelAdd() {
        this.resetAdd();
        this.dialogVisible = false;
      },
      //取消编辑
      cancelEdit(){
        this.resetEdit();
        this.editGroupDialogVisible = false;
      },
      //重置用户组编辑
      resetEdit() {
        this.groupEditForm.group_name = '';
        this.groupEditForm.id = '';
      },
      //重置添加用户组表单信息按钮
      resetAdd() {
        this.groupAddForm.group_desc = '';
        this.groupAddForm.group_name = '';
        this.groupAddForm.group_code = '';
        this.groupAddForm.pid = '';
        this.groupAddForm.valid_status = 'Y';
      },
      //过滤用户组
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
      formatterDate(row, column, cellValue) {
        return Utils.formatDate(new Date(cellValue), 'yyyy-MM-dd')
      },
    },


    /**
     * 属性定义
     * */
    data() {
      // 添加/列表用户组相关
      let checkAddGroupName = (rule, value, callback) => {
        if (!value) {
          return callback(new Error('请输入用户组名称'));
        }
        if (value.length > 30) {
          return callback(new Error('长度不能大于30'));
        }
        callback();
      };
      let checkAddGroupDesc = (rule, value, callback) => {
        if (value === '') {
          return callback(new Error('请输入用户组描述信息'));
        }
        if (('' + value) > 40) {
          return callback(new Error('长度不能大于40'));
        }
        callback();
      };
      let checkAddGroupCode = (rule, value, callback) => {
        if (value === '') {
          return callback(new Error('请输入用户组编码'));
        }
        if (('' + value) > 40) {
          return callback(new Error('长度不能大于40'));
        }
        callback();
      };
      return {
        rolesDialogVisible: false,
        rolesSearchForm: {
          role_name: '',
          role_code: '',
          valid_status: '',
          group_id: '',
          rule: {
            role_name: 'like',
            role_code: 'like'
          },
          paging: {
            page_size: 5,
            current_page: 1
          }
        },
        rolesTableData: [],
        rolesMultipleTable: [],
        rolesSearchFormTotalNum: 0,


        usersDialogVisible: false,
        usersSearchForm: {
          login_name: '',
          contact: '',
          nickname: '',
          valid_status: '',
          group_id: '',
          rule: {
            login_name: 'like',
            contact: 'like',
            nickname: 'like'
          },
          paging: {
            page_size: 5,
            current_page: 1
          }
        },
        usersTableData: [],
        usersMultipleTable: [],
        usersSearchFormTotalNum: 0,

        // 用户组-添加/列表/详情相关
        groupAddFormRule: {
          group_name: [
            {validator: checkAddGroupName, trigger: 'blur'}
          ],
          group_desc: [
            {validator: checkAddGroupDesc, trigger: 'blur'}
          ],
          group_code: [
            {validator: checkAddGroupCode, trigger: 'blur'}
          ]
        },
        detailsDialogVisible: false,
        dialogVisible: false,
        groupDetails: {
          group_desc: '',
          group_code: '',
          group_name: ''
        },
        groupAddForm: {
          group_desc: '',
          group_code: '',
          group_name: '',
          pid: '',
          valid_status: 'Y'
        },
        parent_group_name: '',
        default_pname: '顶级用户组',
        filterText: '',
        viewOrEditResFilterText: '',
        groupData: [],
        defaultProps: {
          children: 'children',
          label: 'label'
        },
        viewOrEditResData: [{}],
        viewOrEditResDefaultProps: {
          children: 'children',
          label: 'label'
        },
        viewOrEditResDialogVisible: false,
        viewOrEditResDetailsVisible: false,
        edit_resource_group_id: '',
        current_check_group: '',
        viewOrEditResDetailsPopoverObj: {
          res_name: '',
          res_desc: '',
          res_uri: '',
          res_type: '',
          method: '',
          res_code: '',
        },

        editGroupDialogVisible: false,
        groupEditForm: {
          group_name: '',
          group_desc: '',
          id: ''
        },
        groupEditFormRule: {
          group_name: [
            {validator: checkAddGroupName, trigger: 'blur'}
          ],
          group_desc: [
            {validator: checkAddGroupDesc, trigger: 'blur'}
          ],
        },
        loading: true,
      }
    },
    mounted: function () {
      this.onSearch();
      this.initViewOrEditResData();
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
