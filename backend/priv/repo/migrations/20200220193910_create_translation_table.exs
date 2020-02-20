defmodule Pyairwaves.Repo.Migrations.CreateTranslationTable do
  use Ecto.Migration

  def change do
    create_if_not_exists table(:translation) do
      add :reg, :string, size: 20
      add :reg_correct, :string, size: 20
      add :operator, :string, size: 20
      add :operator_correct, :string, size: 20
      add :source, :string, size: 255
      timestamps()
    end
  end
end
