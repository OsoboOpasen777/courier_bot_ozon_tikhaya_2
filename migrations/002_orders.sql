
create table if not exists orders (
  id bigserial primary key,
  external_id text not null,
  address text not null,
  window_from timestamptz,
  window_to timestamptz,
  status text not null default 'new',
  inserted_at timestamptz default now()
);
create unique index if not exists orders_external_id_uq on orders(external_id);
