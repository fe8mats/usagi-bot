CREATE TABLE `schedule` (
  `id` integer primary key autoincrement,
  `message_id` text,
  `channel_id` text,
  `type` text,
  `title` text,
  `info` text,
  `user_id` text,
  `thumbnail_path` text,
  `deadline` text default null,
  `delete_flg` integer default 0,
  `create_at` text default null,
  `updated_at` text default null,
  `deleted_at` text default null
);