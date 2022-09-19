DROP TABLE IF EXISTS `test`.`post`;
DROP TABLE IF EXISTS `test`.`user`;

CREATE TABLE `test`.`user` (
  `id` INT AUTO_INCREMENT,
  `username` VARCHAR(100) UNIQUE NOT NULL,
  `password` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE `test`.`post` (
  `id` INTEGER AUTO_INCREMENT,
  `author_id` INT NOT NULL,
  `created` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `title` VARCHAR(100) NOT NULL,
  `body` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`author_id`) REFERENCES `test`.`user`(`id`)
);
