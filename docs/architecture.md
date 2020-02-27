# pyAirwaves architecture

## Summary
This new architecture permits a more real scalability than the python backend wouldn't have permitted.

## Data ingesters
They are currently written in Python, the `libPyairwaves` is here to avoid duplicating code, and mainly handling the JSON structures.

## Backend
The backend is built around the [Phoenix Framework](https://www.phoenixframework.org/) and [Ecto](https://github.com/elixir-ecto/ecto), using the [Elixir](https://elixir-lang.org/) language.

## PubSub(s)
We have two PubSub systems present.

- The Redis one, used between the backend and multiple data ingesters, the PubSub room is called `room:vehicles`, the messages are JSON dicts, see the file `json_vehicles.md` for documentation about the structure.

- The Elixir PG2 one, used internally inside Elixir and will listen to `Redis(room:vehicles)` and broadcast to any connected WebSocket to the channel `room:vehicles`, it broadcasts the JSON messages without transformations.

## Frontend
Located in `backend/priv/static/` for the JavaScript and CSS parts.

And under `backend/lib/pyairwaves_web/templates/` for the HTML templates.

It uses JQuery, Leaflet (plus various libraries) and bootstrap mainly.

The WebSocket is using a special protocol [from the Phoenix framework](https://hexdocs.pm/phoenix/js/), a single websocket is used to multiplex multiple channels.
