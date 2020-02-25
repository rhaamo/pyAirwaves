defmodule Pyairwaves.ArchiveShip do
  use Ecto.Schema
  import Ecto.Changeset

  @primary_key {:id, :id, autogenerate: true}

  schema "archive_ship" do
    field :address, :string
    field :icao_aacc, :string

    # has_many :archive_ship_messages, Pyairwaves.ArchiveShipMessage

    timestamps()
  end

  @doc false
  def changeset(aircraft, attrs) do
    aircraft
    |> cast(attrs, [
      :icao,
      :mmsi_type,
      :mmsi_cc,
      :callsign,
      :dim_to_bow,
      :dim_to_stern,
      :dim_to_port,
      :dim_to_starboard,
      :ship_type
    ])
    |> validate_required([:mmsi, :mmsi_type])
    |> unique_constraint(:mmsi)
    |> unique_constraint(:callsign)
  end
end
