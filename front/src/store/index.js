
import Vue from 'vue'
import Vuex from 'vuex'
import mutations from './mutations'
import actions from './actions'

Vue.use(Vuex);

const state = {
  side_menus: [], // 侧边栏菜单列表
  nav_menus: [], //导航菜单列表

};

export default new Vuex.Store({
    state,
    mutations,
    actions
})
