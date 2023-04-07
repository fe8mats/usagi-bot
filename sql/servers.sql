CREATE TABLE `servers` (
  `id` integer primary key autoincrement,
  `slug` text,
  `title` text,
  `host` text,
  `port` text,
  `password` text,
  `message` text,
  `manager` text,
  `delete_flg` integer default 0,
  `create_at` text default null,
  `updated_at` text default null,
  `deleted_at` text default null
);