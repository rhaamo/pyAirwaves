defmodule Pyairwaves.ArchiveSource do
  use Ecto.Schema
  import Ecto.Changeset

  @primary_key {:id, :id, autogenerate: true}

  schema "archive_source" do
    field :name, :string
    field :type, :string
    field :geom, Geo.PostGIS.Geometry
    # see docs/PubSub_structure srcPosMode list
    field :position_mode, :integer, default: 0
    field :entrypoint, :string
    field :data_origin, :string

    has_many :archive_ship_messages, Pyairwaves.ArchiveShipMessage
    has_many :archive_aircraft_messages, Pyairwaves.ArchiveShipMessage

    timestamps()
  end

  @doc false
  def changeset(aircraft, attrs) do
    aircraft
    |> cast(attrs, [:name, :geom, :position_mode])
    |> validate_required([:name, :type])
    |> unique_constraint([:name, :type])
  end
end
