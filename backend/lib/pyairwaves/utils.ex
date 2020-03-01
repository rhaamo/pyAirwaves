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

  def bearing_to_degrees(bearing) do
    degrees = round(Math.rad2deg(bearing))
    rem(degrees + 360, 360)
  end

  def bearing_to_direction(bearing) do
    case bearing do
      bearing when bearing == 360 or (bearing >= 0 and bearing < 22.5 ) -> %{degree: bearing, shortname: "N", fullname: "North"}
      bearing when bearing >= 22.5 and bearing < 45 -> %{degree: bearing, shortname: "NNE", fullname: "North-Northeast"}
      bearing when bearing >= 45 and bearing < 67.5 -> %{degree: bearing, shortname: "NE", fullname: "Northeast"}
      bearing when bearing >= 67.5 and bearing < 90 -> %{degree: bearing, shortname: "ENE", fullname: "East-Northeast"}
      bearing when bearing >= 90 and bearing < 112.5 -> %{degree: bearing, shortname: "E", fullname: "East"}
      bearing when bearing >= 112.5 and bearing < 135 -> %{degree: bearing, shortname: "ESE", fullname: "East-Southeast"}
      bearing when bearing >= 135 and bearing < 157.5 -> %{degree: bearing, shortname: "SE", fullname: "Southeast"}
      bearing when bearing >= 157.5 and bearing < 180 -> %{degree: bearing, shortname: "SSE", fullname: "South-Southeast"}
      bearing when bearing >= 180 and bearing < 202.5 -> %{degree: bearing, shortname: "S", fullname: "South"}
      bearing when bearing >= 202.5 and bearing < 225 -> %{degree: bearing, shortname: "SSW", fullname: "South-Southwest"}
      bearing when bearing >= 225 and bearing < 247.5 -> %{degree: bearing, shortname: "SW", fullname: "Southwest"}
      bearing when bearing >= 247.5 and bearing < 270 -> %{degree: bearing, shortname: "WSW", fullname: "West-Southwest"}
      bearing when bearing >= 270 and bearing < 292.5 -> %{degree: bearing, shortname: "W", fullname: "West"}
      bearing when bearing >= 292.5 and bearing < 315 -> %{degree: bearing, shortname: "WNW", fullname: "West-Northwest"}
      bearing when bearing >= 315 and bearing < 337.5 -> %{degree: bearing, shortname: "NW", fullname: "Northwest"}
      bearing when bearing >= 337.5 and bearing < 360 -> %{degree: bearing, shortname: "NNW", fullname: "North-Northwest"}
    end
  end
end
