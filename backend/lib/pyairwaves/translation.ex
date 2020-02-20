defmodule Pyairwaves.Translation do
  use Ecto.Schema
  import Ecto.Changeset

  @primary_key {:id, :id, autogenerate: true}

  schema "translation" do
    field :reg, :string, size: 20
    field :reg_correct, :string, size: 20
    field :operator, :string, size: 20
    field :operator_correct, :string, size: 20
    field :source, :string, size: 255
    timestamps()
  end

  @doc false
  def changeset(translation, attrs) do
    translation
    |> cast(attrs, [:reg, :reg_correct, :operator, :operator_correct, :source])
    |> validate_required([:reg, :reg_correct, :operator, :operator_correct, :source])
  end
end
