defmodule Pyairwaves.ArchiveShipMessage.Msg5 do
  use Ecto.Schema

  # AIS Class A Ship Static And Voyage Related Data
  embedded_schema do
    # AIS
    field :ais_version_indicator, :integer
    field :call_sign, :string
    field :destination, :string
    field :dimension_a, :integer
    field :dimension_b, :integer
    field :dimension_c, :integer
    field :dimension_d, :integer
    field :dte, :integer

    embeds_one :eta, Pyairwaves.ArchiveShipMessage.Msg5.Eta do
      field :day, :integer
      field :hour, :integer
      field :minute, :integer
      field :month, :integer
    end

    field :imo_number, :integer
    field :maximum_present_static_draught, :float
    field :name, :string
    field :repeat_indicator, :integer
    field :spare, :integer
    field :type_of_electronic_position_fixing_device, :integer
    field :type_of_ship_and_cargo_type, :integer
    field :user_id, :integer

    # NMEA
    field :channel, :string
    field :checksum, :string
    field :current, :string
    field :formatter, :string
    field :message_id, :integer
    field :padding, :string
    field :payload, :string
    field :talker, :string
    field :total, :string
    field :sequential, :string

  end
end
