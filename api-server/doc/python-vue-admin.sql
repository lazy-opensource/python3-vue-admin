/*
Navicat MySQL Data Transfer

Source Server         : localhost
Source Server Version : 50639
Source Host           : localhost:3306
Source Database       : python-vue-admin

Target Server Type    : MYSQL
Target Server Version : 50639
File Encoding         : 65001

Date: 2018-05-16 23:27:26
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for t_example
-- ----------------------------
DROP TABLE IF EXISTS `t_example`;
CREATE TABLE `t_example` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `valid_status` varchar(5) NOT NULL,
  `create_time` datetime NOT NULL,
  `last_update_time` datetime NOT NULL,
  `name` varchar(30) DEFAULT NULL,
  `age` int(11) DEFAULT NULL,
  `email` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10000 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of t_example
-- ----------------------------
INSERT INTO `t_example` VALUES ('1', 'Y', '2018-04-17 11:44:38', '2018-04-17 11:44:38', 'lisi', '29', '10594463@qq.com');
INSERT INTO `t_example` VALUES ('2', 'Y', '2018-04-17 11:44:38', '2018-04-17 11:44:38', 'chengxi', '38', '16566760594463@qq.com');
INSERT INTO `t_example` VALUES ('3', 'Y', '2018-04-17 11:44:38', '2018-04-17 11:44:38', 'chenghai', '21', '7866510594463@qq.com');
INSERT INTO `t_example` VALUES ('4', 'N', '2018-04-17 11:44:38', '2018-05-16 21:33:33', 'zhaoliu', '32', '1059477777463@qq.com');
INSERT INTO `t_example` VALUES ('5', 'Y', '2018-04-17 11:44:38', '2018-04-17 11:44:38', 'wangwu', '26', '10594463@qq.com');
INSERT INTO `t_example` VALUES ('6', 'Y', '2018-04-17 11:44:38', '2018-04-17 11:44:38', 'lisi', '25', '10594463@qq.com');

-- ----------------------------
-- Table structure for t_permissions_group
-- ----------------------------
DROP TABLE IF EXISTS `t_permissions_group`;
CREATE TABLE `t_permissions_group` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `pid` bigint(20) NOT NULL DEFAULT '-1' COMMENT '父级用户组id',
  `group_name` varchar(30) NOT NULL DEFAULT '' COMMENT '用户组名称',
  `group_desc` varchar(40) NOT NULL DEFAULT '' COMMENT '用户组描述',
  `group_code` varchar(40) DEFAULT '' COMMENT '用户组code',
  `can_edit` varchar(5) NOT NULL DEFAULT 'Y' COMMENT '数据是否可以编辑 Y 可以 N 不可以',
  `valid_status` varchar(5) NOT NULL DEFAULT 'Y' COMMENT '数据有效状态',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `last_update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最后修改时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_group_code` (`group_desc`)
) ENGINE=InnoDB AUTO_INCREMENT=10031 DEFAULT CHARSET=utf8 COMMENT='系统权限-用户组表';

-- ----------------------------
-- Records of t_permissions_group
-- ----------------------------
INSERT INTO `t_permissions_group` VALUES ('1', '-1', '超级管理员组', '超级管理员组（系统默认数据）', 'ADMIN', 'N', 'Y', '2018-04-17 15:05:43', '2018-05-12 21:04:30');
INSERT INTO `t_permissions_group` VALUES ('10029', '-1', '测试用户组', '供测试使用', 'CESHIGROUP', 'Y', 'Y', '2018-05-13 11:47:45', '2018-05-13 11:47:45');
INSERT INTO `t_permissions_group` VALUES ('10030', '1', '管理员用户组', '管理系统人员', 'MANAGERGROUP', 'Y', 'N', '2018-05-13 11:48:24', '2018-05-13 11:48:24');

-- ----------------------------
-- Table structure for t_permissions_resource
-- ----------------------------
DROP TABLE IF EXISTS `t_permissions_resource`;
CREATE TABLE `t_permissions_resource` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `pid` bigint(20) NOT NULL DEFAULT '-1' COMMENT '父级资源',
  `res_name` varchar(50) NOT NULL DEFAULT '' COMMENT '资源名称',
  `res_desc` varchar(50) NOT NULL DEFAULT '' COMMENT '资源描述',
  `res_code` varchar(60) NOT NULL DEFAULT '' COMMENT '资源编码',
  `res_order` int(5) NOT NULL DEFAULT '0' COMMENT '排序',
  `method` varchar(10) NOT NULL DEFAULT '' COMMENT '请求方式',
  `icon` varchar(50) NOT NULL DEFAULT '&#xe62d;' COMMENT '资源图标',
  `uri` varchar(100) NOT NULL DEFAULT '' COMMENT '资源URI',
  `res_type` varchar(20) NOT NULL DEFAULT 'menu' COMMENT '资源类型menu:菜单uri:后台路由',
  `can_edit` varchar(5) NOT NULL DEFAULT 'Y' COMMENT '数据是否可以编辑 Y 可以 N 不可以',
  `valid_status` varchar(20) NOT NULL DEFAULT 'Y' COMMENT '数据有效性',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `last_update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最后修改时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_res_code` (`res_code`)
) ENGINE=InnoDB AUTO_INCREMENT=10020 DEFAULT CHARSET=utf8 COMMENT='系统权限-权限资源表';

-- ----------------------------
-- Records of t_permissions_resource
-- ----------------------------
INSERT INTO `t_permissions_resource` VALUES ('1', '-1', '系统管理', '系统管理', 'root_menu_permissions', '0', '', 'el-icon-menu', '', 'menu', 'N', 'Y', '2018-03-15 11:46:44', '2018-03-15 11:46:44');
INSERT INTO `t_permissions_resource` VALUES ('2', '1', '账号管理', '账号管理', 'menu_permissions_account', '0', '', 'el-icon-menu', '/permissions/users', 'menu', 'N', 'Y', '2018-03-15 11:48:12', '2018-05-12 21:11:16');
INSERT INTO `t_permissions_resource` VALUES ('3', '1', '权限资源管理', '权限资源管理', 'menu_permissions_resource', '0', '', 'el-icon-menu', '/permissions/resources', 'menu', 'N', 'Y', '2018-03-15 11:52:55', '2018-03-15 11:52:55');
INSERT INTO `t_permissions_resource` VALUES ('4', '1', '用户组管理', '用户组管理', 'menu_permissions_group', '0', '', 'el-icon-menu', '/permissions/groups', 'menu', 'N', 'Y', '2018-03-15 11:53:45', '2018-03-15 11:53:45');
INSERT INTO `t_permissions_resource` VALUES ('5', '1', '角色管理', '角色管理', 'menu_permissions_role', '0', '', 'el-icon-menu', '/permissions/roles', 'menu', 'N', 'Y', '2018-03-15 11:54:08', '2018-03-15 11:54:08');
INSERT INTO `t_permissions_resource` VALUES ('6', '1', 'Example', '例子', 'menu_permissions_example', '0', '', 'el-icon-menu', '/examples', 'menu', 'N', 'Y', '2018-05-09 22:42:58', '2018-05-09 22:42:58');
INSERT INTO `t_permissions_resource` VALUES ('10001', '-1', '订单中心', '订单中心', 'root_menu_order', '0', '', 'el-icon-menu', '', 'menu', 'Y', 'Y', '2018-03-15 11:47:31', '2018-03-15 11:47:31');
INSERT INTO `t_permissions_resource` VALUES ('10002', '-1', '用户中心', '用户中心', 'root_menu_user', '0', '', 'el-icon-menu', '', 'menu', 'Y', 'Y', '2018-03-15 11:47:43', '2018-03-15 11:47:43');
INSERT INTO `t_permissions_resource` VALUES ('10007', '-1', '库存中心', '库存中心', 'root_menu_stock', '0', '', 'el-icon-menu', '', 'menu', 'Y', 'Y', '2018-03-15 15:41:13', '2018-03-15 15:41:13');
INSERT INTO `t_permissions_resource` VALUES ('10008', '-1', '价格中心', '价格中心', 'root_menu_price', '0', '', 'el-icon-menu', '', 'menu', 'Y', 'Y', '2018-03-15 15:41:26', '2018-03-15 15:41:26');
INSERT INTO `t_permissions_resource` VALUES ('10009', '-1', '文档管理', '文档管理', 'root_menu_doc', '0', '', 'el-icon-menu', '', 'menu', 'Y', 'Y', '2018-03-15 15:42:02', '2018-03-15 15:42:02');
INSERT INTO `t_permissions_resource` VALUES ('10010', '-1', '日志中心', '系统日志（系统日志记录）', 'root_menu_log', '100', '', 'el-icon-menu', '/permissions/logs', 'menu', 'Y', 'Y', '2018-03-15 15:42:13', '2018-05-12 21:22:02');

-- ----------------------------
-- Table structure for t_permissions_res_group_rel
-- ----------------------------
DROP TABLE IF EXISTS `t_permissions_res_group_rel`;
CREATE TABLE `t_permissions_res_group_rel` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `rid` bigint(20) NOT NULL COMMENT '资源表主键',
  `gid` bigint(20) NOT NULL COMMENT '用户组主键',
  `can_edit` varchar(5) NOT NULL DEFAULT 'Y' COMMENT '数据是否可以编辑 Y 可以 N 不可以',
  `valid_status` varchar(5) NOT NULL DEFAULT 'Y' COMMENT '数据有效性Y:有效N:无效',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `last_update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最后修改时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10101 DEFAULT CHARSET=utf8 COMMENT='系统权限-资源和用户组多对多关联关系表';

-- ----------------------------
-- Records of t_permissions_res_group_rel
-- ----------------------------
INSERT INTO `t_permissions_res_group_rel` VALUES ('10083', '1', '1', 'Y', 'Y', '2018-05-12 09:51:19', '2018-05-12 09:51:19');
INSERT INTO `t_permissions_res_group_rel` VALUES ('10084', '2', '1', 'Y', 'Y', '2018-05-12 09:51:19', '2018-05-12 09:51:19');
INSERT INTO `t_permissions_res_group_rel` VALUES ('10085', '3', '1', 'Y', 'Y', '2018-05-12 09:51:19', '2018-05-12 09:51:19');
INSERT INTO `t_permissions_res_group_rel` VALUES ('10086', '4', '1', 'Y', 'Y', '2018-05-12 09:51:19', '2018-05-12 09:51:19');
INSERT INTO `t_permissions_res_group_rel` VALUES ('10087', '5', '1', 'Y', 'Y', '2018-05-12 09:51:19', '2018-05-12 09:51:19');
INSERT INTO `t_permissions_res_group_rel` VALUES ('10088', '6', '1', 'Y', 'Y', '2018-05-12 09:51:19', '2018-05-12 09:51:19');
INSERT INTO `t_permissions_res_group_rel` VALUES ('10089', '10001', '1', 'Y', 'Y', '2018-05-12 09:51:19', '2018-05-12 09:51:19');
INSERT INTO `t_permissions_res_group_rel` VALUES ('10090', '10007', '1', 'Y', 'Y', '2018-05-12 09:51:19', '2018-05-12 09:51:19');
INSERT INTO `t_permissions_res_group_rel` VALUES ('10091', '10008', '1', 'Y', 'Y', '2018-05-12 09:51:19', '2018-05-12 09:51:19');
INSERT INTO `t_permissions_res_group_rel` VALUES ('10092', '10009', '1', 'Y', 'Y', '2018-05-12 09:51:19', '2018-05-12 09:51:19');
INSERT INTO `t_permissions_res_group_rel` VALUES ('10093', '10010', '1', 'Y', 'Y', '2018-05-12 09:51:19', '2018-05-12 09:51:19');
INSERT INTO `t_permissions_res_group_rel` VALUES ('10100', '10001', '10029', 'Y', 'Y', '2018-05-16 23:15:20', '2018-05-16 23:15:20');

-- ----------------------------
-- Table structure for t_permissions_res_role_rel
-- ----------------------------
DROP TABLE IF EXISTS `t_permissions_res_role_rel`;
CREATE TABLE `t_permissions_res_role_rel` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `res_id` bigint(20) NOT NULL COMMENT '资源表主键',
  `role_id` bigint(20) NOT NULL COMMENT '角色表主键',
  `allocated` varchar(10) NOT NULL DEFAULT 'CAN' COMMENT 'CAN: 可以再次配置 CAN_NOT：不可以再次配置',
  `auth_type` varchar(10) NOT NULL DEFAULT 'CAN' COMMENT '是否可再分配',
  `can_edit` varchar(5) NOT NULL DEFAULT 'Y' COMMENT '数据是否可以编辑 Y 可以 N 不可以',
  `valid_status` varchar(5) NOT NULL DEFAULT 'Y' COMMENT '数据有效状态 Y:有效 N:无效',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `last_update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最后修改时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10074 DEFAULT CHARSET=utf8 COMMENT='系统权限-资源和角色多对多关联关系表';

-- ----------------------------
-- Records of t_permissions_res_role_rel
-- ----------------------------
INSERT INTO `t_permissions_res_role_rel` VALUES ('10065', '1', '1', 'CAN', 'CAN', 'Y', 'Y', '2018-05-16 23:25:05', '2018-05-16 23:25:05');
INSERT INTO `t_permissions_res_role_rel` VALUES ('10066', '2', '1', 'CAN', 'CAN', 'Y', 'Y', '2018-05-16 23:25:05', '2018-05-16 23:25:05');
INSERT INTO `t_permissions_res_role_rel` VALUES ('10067', '3', '1', 'CAN', 'CAN', 'Y', 'Y', '2018-05-16 23:25:05', '2018-05-16 23:25:05');
INSERT INTO `t_permissions_res_role_rel` VALUES ('10068', '4', '1', 'CAN', 'CAN', 'Y', 'Y', '2018-05-16 23:25:05', '2018-05-16 23:25:05');
INSERT INTO `t_permissions_res_role_rel` VALUES ('10069', '5', '1', 'CAN', 'CAN', 'Y', 'Y', '2018-05-16 23:25:05', '2018-05-16 23:25:05');
INSERT INTO `t_permissions_res_role_rel` VALUES ('10070', '6', '1', 'CAN', 'CAN', 'Y', 'Y', '2018-05-16 23:25:05', '2018-05-16 23:25:05');
INSERT INTO `t_permissions_res_role_rel` VALUES ('10071', '10008', '1', 'CAN', 'CAN', 'Y', 'Y', '2018-05-16 23:25:05', '2018-05-16 23:25:05');
INSERT INTO `t_permissions_res_role_rel` VALUES ('10072', '10009', '1', 'CAN', 'CAN', 'Y', 'Y', '2018-05-16 23:25:05', '2018-05-16 23:25:05');
INSERT INTO `t_permissions_res_role_rel` VALUES ('10073', '10010', '1', 'CAN', 'CAN', 'Y', 'Y', '2018-05-16 23:25:05', '2018-05-16 23:25:05');

-- ----------------------------
-- Table structure for t_permissions_role
-- ----------------------------
DROP TABLE IF EXISTS `t_permissions_role`;
CREATE TABLE `t_permissions_role` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `pid` bigint(20) NOT NULL DEFAULT '-1' COMMENT '上级角色id',
  `role_name` varchar(30) NOT NULL DEFAULT '' COMMENT '角色名称',
  `role_code` varchar(40) NOT NULL COMMENT '角色编码',
  `can_edit` varchar(5) NOT NULL DEFAULT 'Y' COMMENT '数据是否可以编辑 Y 可以 N 不可以',
  `valid_status` varchar(5) NOT NULL DEFAULT 'Y' COMMENT '数据有效状态Y:有效N:无效',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `last_update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最后修改时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_role_code` (`role_code`)
) ENGINE=InnoDB AUTO_INCREMENT=10009 DEFAULT CHARSET=utf8 COMMENT='系统权限-角色表';

-- ----------------------------
-- Records of t_permissions_role
-- ----------------------------
INSERT INTO `t_permissions_role` VALUES ('1', '-1', '超级管理员', 'ADMIN', 'N', 'Y', '2018-04-17 15:04:14', '2018-04-17 15:04:14');
INSERT INTO `t_permissions_role` VALUES ('10000', '-1', '测试角色', 'TEST', 'Y', 'Y', '2018-05-13 21:24:35', '2018-05-13 21:24:35');
INSERT INTO `t_permissions_role` VALUES ('10003', '-1', 'yyy', 'yyy', 'Y', 'Y', '2018-05-16 21:06:02', '2018-05-16 21:06:02');
INSERT INTO `t_permissions_role` VALUES ('10006', '-1', 'kkk', 'kkk', 'Y', 'Y', '2018-05-16 21:06:23', '2018-05-16 21:34:30');
INSERT INTO `t_permissions_role` VALUES ('10008', '-1', 'kkkk', 'kkkk', 'Y', 'Y', '2018-05-16 21:35:58', '2018-05-16 21:35:58');

-- ----------------------------
-- Table structure for t_permissions_role_group_rel
-- ----------------------------
DROP TABLE IF EXISTS `t_permissions_role_group_rel`;
CREATE TABLE `t_permissions_role_group_rel` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `rid` bigint(20) NOT NULL COMMENT '角色表主键',
  `gid` bigint(20) NOT NULL COMMENT '用户组表主键',
  `can_edit` varchar(5) NOT NULL DEFAULT 'Y' COMMENT '数据是否可以编辑 Y 可以 N 不可以',
  `valid_status` varchar(5) NOT NULL DEFAULT 'Y' COMMENT '数据有效状态 Y:有效 N:无效',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `last_update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最后修改时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10004 DEFAULT CHARSET=utf8 COMMENT='系统权限-角色和用户组多对多关联关系';

-- ----------------------------
-- Records of t_permissions_role_group_rel
-- ----------------------------
INSERT INTO `t_permissions_role_group_rel` VALUES ('10000', '1', '1', 'N', 'Y', '2018-04-17 15:06:58', '2018-04-17 15:06:58');
INSERT INTO `t_permissions_role_group_rel` VALUES ('10001', '10000', '10029', 'Y', 'Y', '2018-05-13 21:25:03', '2018-05-13 21:25:03');
INSERT INTO `t_permissions_role_group_rel` VALUES ('10003', '10008', '10029', 'Y', 'Y', '2018-05-16 22:25:32', '2018-05-16 22:25:32');

-- ----------------------------
-- Table structure for t_permissions_user
-- ----------------------------
DROP TABLE IF EXISTS `t_permissions_user`;
CREATE TABLE `t_permissions_user` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `nickname` varchar(50) NOT NULL COMMENT '昵称',
  `password` varchar(200) NOT NULL COMMENT '密码',
  `salt` varchar(40) NOT NULL COMMENT '加密盐',
  `login_name` varchar(60) NOT NULL COMMENT '登录名称',
  `can_edit` varchar(5) NOT NULL DEFAULT 'Y' COMMENT '数据是否可以编辑 Y 可以 N 不可以',
  `valid_status` varchar(5) NOT NULL DEFAULT 'Y' COMMENT '数据有效状态 Y:有效 N:无效',
  `contact` varchar(20) NOT NULL DEFAULT '' COMMENT '联系方式',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `last_update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最后一次修改时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_user_name` (`login_name`) USING BTREE COMMENT '邮箱不能重复',
  UNIQUE KEY `uniq_login_name` (`login_name`)
) ENGINE=InnoDB AUTO_INCREMENT=10008 DEFAULT CHARSET=utf8 COMMENT='系统权限-用户表';

-- ----------------------------
-- Records of t_permissions_user
-- ----------------------------
INSERT INTO `t_permissions_user` VALUES ('1', '超级管理员', 'pbkdf2:sha256:50000$I4VHIE58$00b930d5a9774a83960acbb01b0c59fe224d6175b356eef041715e4ed8bde801', 'b503bc0a55f011e88851000000000001', 'admin', 'N', 'Y', '13652365899', '2018-04-17 15:03:50', '2018-04-17 15:03:50');
INSERT INTO `t_permissions_user` VALUES ('10001', 'test', 'pbkdf2:sha256:50000$h3B1WCY2$42b9e9811b6f0d1799f277bc59f870494a207f861efbf6be4c5edf331053d03e', '14c43bf455f011e88f97000000000001', 'test', 'Y', 'N', '13232323232', '2018-05-12 22:23:46', '2018-05-16 21:33:46');

-- ----------------------------
-- Table structure for t_permissions_user_group_rel
-- ----------------------------
DROP TABLE IF EXISTS `t_permissions_user_group_rel`;
CREATE TABLE `t_permissions_user_group_rel` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `uid` bigint(20) NOT NULL COMMENT '用户主键',
  `gid` bigint(20) NOT NULL COMMENT '用户组主键',
  `can_edit` varchar(5) NOT NULL DEFAULT 'Y' COMMENT '数据是否可以编辑 Y 可以 N 不可以',
  `valid_status` varchar(5) CHARACTER SET utf8 NOT NULL DEFAULT 'Y' COMMENT '数据有效性Y:有效N:无效',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `last_update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最后修改时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10024 DEFAULT CHARSET=sjis COMMENT='系统权限-用户和用户组多对多关系表';

-- ----------------------------
-- Records of t_permissions_user_group_rel
-- ----------------------------
INSERT INTO `t_permissions_user_group_rel` VALUES ('10000', '1', '1', 'N', 'Y', '2018-05-13 17:58:27', '2018-05-13 17:58:27');
INSERT INTO `t_permissions_user_group_rel` VALUES ('10023', '10001', '10029', 'Y', 'Y', '2018-05-13 20:26:23', '2018-05-13 20:26:23');

-- ----------------------------
-- Table structure for t_permissions_user_role_rel
-- ----------------------------
DROP TABLE IF EXISTS `t_permissions_user_role_rel`;
CREATE TABLE `t_permissions_user_role_rel` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `uid` bigint(20) NOT NULL COMMENT '用户表主键',
  `rid` bigint(20) NOT NULL COMMENT '角色表主键',
  `can_edit` varchar(5) NOT NULL DEFAULT 'Y' COMMENT '数据是否可以编辑 Y 可以 N 不可以',
  `valid_status` varchar(5) NOT NULL DEFAULT 'Y' COMMENT '数据有效状态',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `last_update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最后更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10006 DEFAULT CHARSET=utf8 COMMENT='系统权限-用户和角色关联关系表';

-- ----------------------------
-- Records of t_permissions_user_role_rel
-- ----------------------------
INSERT INTO `t_permissions_user_role_rel` VALUES ('10000', '1', '1', 'N', 'Y', '2018-05-13 21:43:32', '2018-05-13 21:43:32');
INSERT INTO `t_permissions_user_role_rel` VALUES ('10005', '10001', '10000', 'Y', 'Y', '2018-05-13 21:47:02', '2018-05-13 21:47:02');
