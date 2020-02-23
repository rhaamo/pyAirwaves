defmodule Pyairwaves.Utils do

  @doc "Return acc with key=value if value defined else returns acc untouched"
  def put_if(acc, key, value) do
    case value do
      n when n in ["", nil] -> acc
      n -> Map.put(acc, key, n)
    end
  end
end
