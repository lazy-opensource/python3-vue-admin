<template>
  <el-row :gutter="10">
    <div class="bg-color">
      <app-login-header></app-login-header>
      <el-col :offset="6" :xs="12" :sm="12" :md="12" :lg="12" :xl="12"><div class="pad grid-content bg-purple">
        <el-alert
          title="权限不足提示"
          @close="close"
          type="warning"
          description="您没有访问该资源的权限"
          close-text="返回"
          show-icon>
        </el-alert>
      </div></el-col>
    </div>
  </el-row>
</template>

<script>
  import appLoginHeader from '../components/login-header'
    export default {
      name: "appPermissionDenied",
      components: {
        appLoginHeader
      },
      methods: {
        close: function () {
          this.$router.go(-1)
        }
      }
    }
</script>

<style scoped>
.bg-color {
  background: linear-gradient(#012B75, red);
  height: 100vh;
}
  .pad{
    padding-top: 200px;
  }
</style>
