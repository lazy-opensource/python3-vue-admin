<template>
  <el-row :gutter="10">
    <div class="bg-color">
      <app-login-header></app-login-header>
      <el-col :offset="6" :xs="12" :sm="12" :md="12" :lg="12" :xl="12"><div class="pad grid-content bg-purple">
        <el-alert
          title="不合法"
          @close="close"
          type="warning"
          description="请合法操作，做个良好公民"
          show-icon>
        </el-alert>
      </div></el-col>
    </div>
  </el-row>
</template>

<script>
  import appLoginHeader from '../components/login-header'
  export default {
    name: "appNotLegal",
    components: {
      appLoginHeader
    },
    methods: {

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
