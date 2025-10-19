create table if not exists topics (
  chat_id   bigint not null,
  thread_id integer not null,
  name      text default '',
  inserted_at timestamptz default now(),
  primary key (chat_id, thread_id)
);

-- если есть колонка "trhead_id" — переименуем
do $$
begin
  if exists (
    select 1 from information_schema.columns
    where table_name='topics' and column_name='trhead_id'
  ) then
    alter table topics rename column trhead_id to thread_id;
  end if;
end $$;
