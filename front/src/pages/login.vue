<template>
  <el-row :gutter="10">
    <div class="bg-color">
      <app-login-header></app-login-header>
    <el-col :offset="6" :xs="8" :sm="12" :md="12" :lg="12" :xl="12"><div class="main grid-content bg-purple">
      <el-form :model="loginForm" status-icon :rules="login" ref="loginForm" label-width="100px" class="demo-ruleForm">
        <el-form-item label="账号" prop="username">
          <el-input type="text" v-model="loginForm.username" auto-complete="on"></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="pass">
          <el-input type="password" v-model="loginForm.pass" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitForm('loginForm')">登录</el-button>
          <el-button @click="resetForm('loginForm')">重置</el-button>
        </el-form-item>
      </el-form>
    </div></el-col>
    </div>
  </el-row>
</template>

<script>
    import * as Constant from "../constant";
    import Utils from "../utils";
    import appLoginHeader from '../components/login-header'

    export default {
      components: {
        appLoginHeader
      },

      data() {
        let checkUsername = (rule, value, callback) => {
          if (!value) {
            return callback(new Error('请输入用户名'));
          }
          callback();
        };
        let validatePass = (rule, value, callback) => {
          if (value === '') {
            callback(new Error('请输入密码'));
          }
          callback();
        };
        return {
          loginForm: {
            pass: '',
            username: '',
            user_type: 'admin'
          },
          login: {
            pass: [
              { validator: validatePass, trigger: 'blur' }
            ],
            username: [
              { validator: checkUsername, trigger: 'blur' }
            ]
          }
        };
      },
      methods: {
        submitForm(formName) {
          const self = this;
          self.$refs[formName].validate((valid) => {
            if (valid) {
              self.$axios.put(Constant.ADMIN_LOGIN_URI, {
                params: this.loginForm
              }).then(function (resp) {
                if (resp.code !== Constant.REQ_SUCCESS){
                  self.$alert(resp.msg, '系统提示');
                }else {
                  Utils.localStorageSet(Constant.TOKEN_KEY, resp.data);
                  self.$router.push("/")
                }
              }).catch(resp => {
                console.log(resp);
                self.$alert('请求出错', '系统提示');
              });
            } else {
              self.$alert('请正确地输入账号和密码', '系统提示');
              return false;
            }
          });
        },
        resetForm(formName) {
          this.$refs[formName].resetFields();
        }
      }
    }
</script>

<style scoped>

  .main {
    padding-top: 130px;
  }
  .bg-color {
    /*animation: name duration timing-function delay iteration-count direction;*/
    height: 100vh;
    background: linear-gradient(#012B75, darkslategray);
   /* animation: changeBkgColor 3s linear 1s infinite;
    -moz-animation: changeBkgColor 3s linear 1s infinite;	!* Firefox *!
    -webkit-animation: changeBkgColor 3s linear 1s infinite;!* Safari 和 Chrome *!
    -o-animation: changeBkgColor 3s linear 1s infinite;	!* Opera *!*/
  }

  /*.bg-color {*/
    /*height: 100vh;*/
    /*background: linear-gradient(#012B75, blue);*/
    /*background: linear-gradient(#012B75, hotpink);*/
    /*background-color: #012B75;*/
    /*transition-property: background-color;*/
    /*transition-timing-function: linear;*/
    /*transition-duration: 3s;*/
    /*transition-delay: 1s;*/

    /*-webkit-transition-property: background-color;*/
    /*-webkit-transition-timing-function: linear;*/
    /*-webkit-transition-duration: 2s;*/
    /*-webkit-transition-delay: 1s;*/
  /*}*/
  /*.bg-color:hover {*/
    /*!*background-color: linear-gradient(#012B75, red);*!*/
    /*background-color: #0D5477;*/
  /*}*/

  /*@keyframes changeBkgColor
  {
    0% {background: linear-gradient(#012B75, hotpink);}
   !* 25% {background: linear-gradient(#012B75, gray);}*!
    50% {background: linear-gradient(#012B75, darkslategray);}
    100% {background: linear-gradient(#012B75, red);}
  }

  @-moz-keyframes changeBkgColor !* Firefox *!
  {
    0% {background: linear-gradient(#012B75, hotpink);}
   !* 25% {background: linear-gradient(#012B75, gray);}*!
    50% {background: linear-gradient(#012B75, darkslategray);}
    100% {background: linear-gradient(#012B75, red);}
  }

  @-webkit-keyframes changeBkgColor !* Safari 和 Chrome *!
  {
    0% {background: linear-gradient(#012B75, hotpink);}
   !* 25% {background: linear-gradient(#012B75, gray);}*!
    50% {background: linear-gradient(#012B75, darkslategray);}
    100% {background: linear-gradient(#012B75, red);}
  }*/

</style>
