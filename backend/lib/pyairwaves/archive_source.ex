defmodule Pyairwaves.ArchiveSource do
  use Ecto.Schema
  import Ecto.Changeset

  @primary_key {:id, :id, autogenerate: true}

  schema "archive_source" do
    field :name, :string
    field :geom, Geo.PostGIS.Geometry
    field :position_mode, :integer, default: 0  # see docs/PubSub_structure srcPosMode list
    field :entrypoint, :string
    field :data_origin, :string

    has_many :archive_ship_messages, Pyairwaves.ArchiveShipMessage

    timestamps()
  end

  @doc false
  def changeset(aircraft, attrs) do
    aircraft
    |> cast(attrs, [:name, :geom, :position_mode])
    |> validate_required([:name])
    |> unique_constraint(:name)
  end
end
