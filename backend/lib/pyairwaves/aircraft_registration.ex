defmodule Pyairwaves.AircraftRegistration do
  use Ecto.Schema
  import Ecto.Changeset

  @primary_key {:id, :id, autogenerate: true}

  # Index on country

  schema "aircraft_registration" do
    field :country, :string, size: 255
    field :prefix, :string, size: 10
  end

  @doc false
  def changeset(aircraft_registration, attrs) do
    aircraft_registration
    |> cast(attrs, [:country, :prefix])
    |> validate_required([:country, :prefix])
  end
end
