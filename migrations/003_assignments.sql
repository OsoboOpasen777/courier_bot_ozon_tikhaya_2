
create table if not exists assignments (
  id bigserial primary key,
  order_id bigint not null references orders(id) on delete cascade,
  courier_id bigint not null references couriers(id) on delete cascade,
  assigned_at timestamptz default now(),
  status text not null default 'assigned'
);
create index if not exists assignments_order_idx on assignments(order_id);
create index if not exists assignments_courier_idx on assignments(courier_id);
