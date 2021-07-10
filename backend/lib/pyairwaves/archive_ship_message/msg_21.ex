defmodule Pyairwaves.ArchiveShipMessage.Msg1 do
  use Ecto.Schema

  # AIS Aids To Navigation (ATON) ReportAIS Aids To Navigation (ATON) Report
  embedded_schema do
    # AIS
    field :assigned_mode_flag, :integer
    field :aton_status, :integer
    field :dimension_a, :integer
    field :dimension_b, :integer
    field :dimension_c, :integer
    field :dimension_d, :integer
    # field :id, :integer
    field :latitude, :float
    field :longitude, :float
    field :name_of_aids_to_navigation, :string
    field :name_extension, :string
    field :assembled_name, :string
    field :off_position_indicator, :integer
    field :position_accuracy, :integer
    field :raim_flag, :integer
    field :repeat_indicator, :integer
    field :spare, :integer
    field :time_stamp, :integer
    field :type_of_aids_to_navigation, :integer
    field :type_of_electronic_position_fixing_device, :integer
    field :virtual_aton_flag, :integer

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
