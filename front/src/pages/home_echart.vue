<template>
 <!-- <el-breadcrumb separator="/">
    <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
    <el-breadcrumb-item>活动管理</el-breadcrumb-item>
    <el-breadcrumb-item>活动列表</el-breadcrumb-item>
    <el-breadcrumb-item>活动详情</el-breadcrumb-item>
  </el-breadcrumb>-->
  <div id="main" ref="myEchart" style="width: 800px;height: 200px;"></div>
</template>

<script>
  import echarts from 'echarts'
  export default {
    name: '',
    data () {
      return {
        chart: null,

      }
    },
    methods:{
      initChart() {
        this.chart = echarts.init(this.$refs.myEchart);
        // 把配置和数据放这里
        this.chart.setOption({
          color: ['#3398DB'],
          tooltip: {
            trigger: 'axis',
            axisPointer: { // 坐标轴指示器，坐标轴触发有效
              type: 'shadow' // 默认为直线，可选为：'line' | 'shadow'
            }
          },
          grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
          },
          xAxis: [{
            type: 'category',
            data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            axisTick: {
              alignWithLabel: true
            }
          }],
          yAxis: [{
            type: 'value'
          }],
          series: [{
            name: '直接访问',
            type: 'bar',
            barWidth: '60%',
            data: [10, 52, 200, 334, 390, 330, 220]
          }]
        })
      }
    },
    //调用
    mounted(){
      this.initChart();
    }
  }
</script>
<style scoped>
  * {
    margin: 0;
    padding: 0;
    list-style: none;
  }
</style>
