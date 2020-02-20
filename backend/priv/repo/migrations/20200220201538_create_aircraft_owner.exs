defmodule Pyairwaves.Repo.Migrations.CreateAircraftOwner do
  use Ecto.Migration

  def change do
    create_if_not_exists table(:aircraft_owner) do
      add :registration, :string
      add :base, :string
      add :owner, :string
      add :date_first_reg, :naive_datetime
      add :source, :string
      add :is_private, :boolean, default: false, null: false
    end

    create index(:aircraft_owner, :registration)

  end
end
