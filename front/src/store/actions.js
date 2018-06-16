import * as types from './mutation_types'

export default {
  click_nav_menu({ commit }, side_menus) {
    commit(types.CLICK_NAV_MENU, side_menus)
  },
}
