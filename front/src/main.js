import Vue from 'vue'
import App from './App'
import router from './router'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import * as axios from "axios";
import store from './store';
import Intercept from "./intercept";
import echarts from 'echarts'
import Utils from "./utils";

Vue.config.productionTip = false;

axios.defaults.baseURL = process.env.ADMIN_DOMAIN;

Intercept.routerBeforeEach(axios, router);
Intercept.requestIntercept(axios, router);
Intercept.responseIntercept(axios, router);
Vue.prototype.$axios = axios;
Vue.prototype.$echarts = echarts;
Vue.filter('formatDate', Utils.formatDate);
Vue.use(ElementUI);

const errorHandler = (error, vm)=>{
  console.error('抛出全局异常');
  console.error(vm);
  console.error(error);
};

Vue.config.errorHandler = errorHandler;
Vue.prototype.$throw = (error)=> errorHandler(error,this);

new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>'
});
