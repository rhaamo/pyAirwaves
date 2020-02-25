defmodule Pyairwaves.ArchiveAircraft do
  use Ecto.Schema
  import Ecto.Changeset

  @primary_key {:id, :id, autogenerate: true}

  schema "archive_aircraft" do
    field :hex_ident, :string

    has_many :archive_aircraft_messages, Pyairwaves.ArchiveAircraftMessage

    # has one aircraft, registration, ...

    timestamps()
  end

  @doc false
  def changeset(aircraft, attrs) do
    aircraft
    |> cast(attrs, [
      :hex_ident
    ])
    |> validate_required([:hex_ident])
    |> unique_constraint(:hex_ident)
  end
end
