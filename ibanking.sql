/*
 Navicat Premium Data Transfer

 Source Server         : mySql
 Source Server Type    : MySQL
 Source Server Version : 100116
 Source Host           : localhost:3306
 Source Schema         : ibanking

 Target Server Type    : MySQL
 Target Server Version : 100116
 File Encoding         : 65001

 Date: 05/03/2021 17:10:49
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for history
-- ----------------------------
DROP TABLE IF EXISTS `history`;
CREATE TABLE `history`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `tuition_id` int NULL DEFAULT NULL,
  `date_of_payment` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `submitter_id` int NULL DEFAULT NULL,
  `receiver_id` int NULL DEFAULT NULL,
  `semester` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 20 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of history
-- ----------------------------
INSERT INTO `history` VALUES (1, 2, '05/03/2020 13:43:34', 51703108, 51703108, '1st semester/ 2020 - 2021');
INSERT INTO `history` VALUES (19, 3, '05/03/2021 17:05:59', 51703108, 51703104, '2nd semester/ 2020 - 2021');

-- ----------------------------
-- Table structure for tuition
-- ----------------------------
DROP TABLE IF EXISTS `tuition`;
CREATE TABLE `tuition`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `semester` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `semester_tuition` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `reduction` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `note` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of tuition
-- ----------------------------
INSERT INTO `tuition` VALUES (1, 1, '2nd semester/ 2020 - 2021', '5400000', '0', 'OWED TUITION FEES');
INSERT INTO `tuition` VALUES (2, 1, '1st semester/ 2020 - 2021', '8000000', '0', 'COMPLETED');
INSERT INTO `tuition` VALUES (3, 2, '2nd semester/ 2020 - 2021', '8000000', '0', 'COMPLETED');
INSERT INTO `tuition` VALUES (4, 3, '2nd semester/ 2020 - 2021', '8000000', '0', 'OWED TUITION FEES');

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(15) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `email` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `password` varchar(80) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `name` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `student_id` varchar(8) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `phone_number` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `money` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `username`(`username`) USING BTREE,
  UNIQUE INDEX `email`(`email`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES (1, 'khailuong', 'khailuong61@gmail.com', 'sha256$84Zxz1q7$027b7309ac3ff526a670603a04bba2707036387a41e69350a6dd6e238490d4f8', 'Lương Quang Khải', '51703108', '0334659620', '20000000');
INSERT INTO `user` VALUES (2, 'bahuy123', 'quangkhai281298@gmail.com', 'sha256$84Zxz1q7$027b7309ac3ff526a670603a04bba2707036387a41e69350a6dd6e238490d4f8', 'Vũ Lưu Bá Huy', '51703104', '0123456789', '5000000');
INSERT INTO `user` VALUES (3, 'hoangkhang', 'khang123@gmail.com', 'sha256$84Zxz1q7$027b7309ac3ff526a670603a04bba2707036387a41e69350a6dd6e238490d4f8', 'Lê Hoàng Khang', '51703109', '0987654321', '7000000');

SET FOREIGN_KEY_CHECKS = 1;
