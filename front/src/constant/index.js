export const TOKEN_KEY = 'python-vue-admin-token';

////////////////////////////////系统模块/////////////////////////////////////////
//系统-登录
export const ADMIN_LOGIN_URI = '/sessions';

//系统权限-用户组
export const ADMIN_PERMISSIONS_GROUPS_URI = '/permissions/groups';
export const ADMIN_PERMISSIONS_GROUP_CHECK_UNIQ = '/permissions/group/check/uniq';
export const ADMIN_PERMISSIONS_GROUP_RESOURCES_BY_GID_URI = '/permissions/group/resourcesbygid';
export const ADMIN_PERMISSIONS_GROUP_RESOURCES_URI = '/permissions/group/resources';
export const ADMIN_PERMISSIONS_GROUP_USERS_URI = '/permissions/group/users';
export const ADMIN_PERMISSIONS_GROUP_ROLES_URI = '/permissions/group/roles';

//系统权限-资源
export const ADMIN_PERMISSIONS_RESOURCES_URI = '/permissions/resources';
export const ADMIN_PERMISSIONS_RESOURCE_CHECK_UNIQ = '/permissions/resource/check/uniq';
export const ADMIN_PERMISSIONS_RESOURCES_BY_ID_URI = '/permissions/resources/id';
export const ADMIN_PERMISSIONS_SUBMENUS_URI = '/permissions/submenus';

//系统权限-用户
export const ADMIN_PERMISSIONS_USERS_URI = '/permissions/users';
export const ADMIN_PERMISSIONS_USER_CHECK_UNIQ = '/permissions/user/check/uniq';
export const ADMIN_PERMISSIONS_USER_GROUPS = '/permissions/user/groups';
export const ADMIN_PERMISSIONS_USER_ROLES = '/permissions/user/roles';
export const ADMIN_PERMISSIONS_USER_ROLES_BY_UID = '/permissions/user/roles/uid';

//系统权限-角色
export const ADMIN_PERMISSIONS_ROLES_URI = '/permissions/roles';
export const ADMIN_PERMISSIONS_ROLE_CHECK_UNIQ = '/permissions/role/check/uniq';
export const ADMIN_PERMISSIONS_ROLE_GROUPS = '/permissions/role/groups';
export const ADMIN_PERMISSIONS_ROLE_RESOURCES = '/permissions/role/resources';
export const ADMIN_PERMISSIONS_ROLE_RESOURCES_BY_RID = '/permissions/role/resources/rid';
////////////////////////////////系统权限模块/////////////////////////////////////////

//例子
export const ADMIN_EXAMPLES_URI = '/examples';

//状态码
export const REQ_SUCCESS = 200;
export const REQ_404 = 404;
export const REQ_400 = 400;
export const REQ_500 = 500;

export const USER_NOT_EXISTS = 1000; //用户不存在
export const PASSWORD_ERROR = 1001; //登录密码错误
export const TOKEN_ERROR = 1002; //token解析错误
export const SALT_ERROR = 1003; //加密盐不正确
export const CLIENT_NOT_LEGAL = 1004; //不合法客户端
export const TOKEN_EXIP = 1005; //token已过期

//前台uri白名单
export const F_URIS_WHITE_LIST = [
  '/login',
  '/permission_denied',
  '/not_legal'
];

//后台uri白名单
export const A_URIS_WHITE_LIST = [
  {'method': 'put', 'uri': '/sessions'},
  {'method': 'delete', 'uri': '/sessions'},
];
