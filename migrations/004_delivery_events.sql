
create table if not exists delivery_events (
  id bigserial primary key,
  order_id bigint not null references orders(id) on delete cascade,
  courier_id bigint not null references couriers(id) on delete cascade,
  event_type text not null,
  payload jsonb default '{}'::jsonb,
  created_at timestamptz default now()
);
create index if not exists delivery_events_order_idx on delivery_events(order_id);
create index if not exists delivery_events_courier_idx on delivery_events(courier_id);
