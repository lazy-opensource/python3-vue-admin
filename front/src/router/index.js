import Vue from 'vue';
import Router from 'vue-router';

Vue.use(Router);

const routes = new Router({
  routes: [
    {path: '/login', component: resolve => require(['../pages/login.vue'], resolve),},
    {path: '/permission_denied', component: resolve => require(['../pages/permission_denied.vue'], resolve)},
    {path: '/not_legal', component: resolve => require(['../pages/not_legal.vue'], resolve)},
    {path: '/', component: resolve => require(['../pages/home.vue'], resolve), children: [
        {path: '', component: resolve => require(['../pages/home_echart.vue'], resolve)},
        {path: 'examples', component: resolve => require(['../pages/example.vue'], resolve)},
        {path: 'permissions/groups', component: resolve => require(['../pages/permissions/group.vue'], resolve)},
        {path: 'permissions/resources', component: resolve => require(['../pages/permissions/resource.vue'], resolve)},
        {path: 'permissions/users', component: resolve => require(['../pages/permissions/user.vue'], resolve)},
        {path: 'permissions/roles', component: resolve => require(['../pages/permissions/role.vue'], resolve)},

      ]
    },
  ]
});

export default routes;
