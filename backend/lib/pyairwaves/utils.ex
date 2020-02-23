defmodule Pyairwaves.Utils do
  @doc "Return acc with key=value if value defined else returns acc untouched"
  def put_if(acc, key, value) do
    case value do
      n when n in ["", nil] -> acc
      n -> Map.put(acc, key, n)
    end
  end

  @doc "Floatizify an Integer"
  def to_float(val) when is_integer(val) do
    val / 1
  end
  def to_float(val) do
    val
  end

  @doc "Returns a Geo.Point from lon/lat"
  def to_geo_point(lon, lat) do
    if is_nil(lon) or is_nil(lat) do
      nil
    else
      %Geo.Point{coordinates: {lon, lat}, srid: 4326}
    end
  end
end
