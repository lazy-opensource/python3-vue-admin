<template>
  <div id="app">
    <el-container>
      <el-header><app-header></app-header></el-header>
      <el-container>
        <el-aside width="250px"><app-side></app-side></el-aside>
        <el-main>
          <router-view></router-view>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
  import appHeader from '../components/main-header';
  import appFooter from '../components/main-footer';
  import appSide from '../components/main-side';
  export default {
    computed:{

    },
    components:{
      appHeader,
      appSide,
      appFooter
    },
    data() {
      return {

      }
    }
  }
</script>

<style scoped>
  .el-header {
    background-color: #143f6d;
    color: #333;
    font-size: x-large;
    margin-bottom: 1px;
    margin-top: 0px;
    text-align: left;
    line-height: 60px;
    padding: 0px;
  }

  .el-aside {
    background-color: #0D5477;
    color: #333;
    line-height: 200px;
    overflow-y:auto;
    width: 180px;
    height: calc(100vh - 80px);
  }
  .el-main {
    background-color: #E9EEF3;
    color: #333;
    text-align: center;
    line-height: 160px;
  }
  .el-footer {
    background-color: #143f6d;
    color: white;
    font-size: x-small;
    text-align: center;
    line-height: 60px;
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
