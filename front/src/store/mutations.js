import * as types from './mutation_types'

export default {
  [types.CLICK_NAV_MENU] (state, side_menus) {
    state.side_menus = side_menus;
    },
  [types.LOAD_NAV_MENU] (state, nav_menus){
    state.nav_menus = nav_menus;
  }
};
