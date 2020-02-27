defmodule Pyairwaves.AircraftOwner do
  use Ecto.Schema
  import Ecto.Changeset

  @primary_key {:id, :id, autogenerate: true}

  # Index on registration

  schema "aircraft_owner" do
    field :base, :string, size: 255, default: nil
    field :date_first_reg, :naive_datetime, default: nil
    field :is_private, :boolean, default: false
    field :owner, :string, size: 255
    field :registration, :string, size: 255
    field :source, :string, size: 255
  end

  @doc false
  def changeset(aircraft_owner, attrs) do
    aircraft_owner
    |> cast(attrs, [:registration, :base, :owner, :date_first_reg, :source, :is_private])
    |> validate_required([:registration, :source])
  end
end
