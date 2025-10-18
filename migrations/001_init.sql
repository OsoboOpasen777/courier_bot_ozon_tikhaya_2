
create table if not exists couriers (
  id bigserial primary key,
  user_id bigint unique not null,
  username text default '',
  full_name text default '',
  real_name text not null,
  phone text default '',
  role text not null default 'courier',
  inserted_at timestamptz default now()
);
create index if not exists couriers_user_id_idx on couriers(user_id);
