
import Utils from "../utils";
import * as Constant from '../constant'
export default {

  // 前台路由前置拦截器
  "routerBeforeEach": function (axios, routes) {
    routes.beforeEach((to, from, next) => {
      // 白名单的路由全部放过
      if (Constant.F_URIS_WHITE_LIST.indexOf(to.path) !== -1){
        next();
        return;
      }
      // 否则检查是否有登录信息
      let loginInfo = Utils.localStorageGet(Constant.TOKEN_KEY);
      // 如果没有登录信息
      if (!loginInfo){
        next('/login');
        return;
      }
      next();
    })
  },

  // 请求后台前置拦截器
  "requestIntercept": function (axios, router) {
    axios.interceptors.request.use(function(config){
      // 白名单的路由全部放过
      for (let i in Constant.A_URIS_WHITE_LIST){
        if (Constant.A_URIS_WHITE_LIST[i]['method'] === config.method.toLowerCase()){
          if (Constant.A_URIS_WHITE_LIST[i]['uri'] === config.url) {
            return config;
          }
        }
      }
      // 否则检查是否有登录信息
      let loginInfo = Utils.localStorageGet(Constant.TOKEN_KEY);
      // 如果没有登录信息
      if (!loginInfo){
        axios.CancelToken.source().cancel();
        router.push('/login');
        return;
      }
      loginInfo = JSON.parse(loginInfo);
      // 如果有登录信息，则继续检查是否有uri权限
      // let uris = loginInfo['uris'];
      // // 如果没有权限
      // if (!Utils.hasAdminUriPermi(uris, config.url, config.method)) {
      //   router.push('/permission_denied');
      //   return;
      // }
      let token = loginInfo['token'];
      let salt = loginInfo['salt'];
      let add_header = {"token": token, "salt": salt};
      config.headers['Py-Vue-Token'] = JSON.stringify(add_header);
      return config;
    },function(err){
      return Promise.reject(err);
    });
  },

  // 后台响应前置拦截器
  "responseIntercept": function (axios, router) {
    const self = this;
    axios.interceptors.response.use(function(res){
      res = res.data;
      if (res.code === Constant.TOKEN_ERROR || res.code === Constant.SALT_ERROR
        || res.code === Constant.CLIENT_NOT_LEGAL){
        router.push("/not_legal")
      }else if (res.code === Constant.TOKEN_EXIP){
        Utils.localStorageSet(Constant.TOKEN_KEY, "");
        axios.CancelToken.source().cancel();
        router.push("/login")
      }else {
        return res;
      }
    },function(err){
      return Promise.reject(err);
    })
  }
}
