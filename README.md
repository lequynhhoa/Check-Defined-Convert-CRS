# Kiểm tra thông tin hệ tọa độ, định nghĩa hệ tọa độ khớp với GE và chuyển hệ tọa độ
Dữ liệu bản đồ của hệ thống ngành Lâm nghiệp hầu hết đều đang ở hệ tọa độ VN2000 Nội bộ, lệch với Google earth 230m. Công cụ này cho phép người dùng chuyển hệ tọa độ, defined hệ tọa độ chồng khớp với Google earth sang định dạng shapefile (.shp)

# Check, Defined and Convert coordinate system
This plugin have 3 functions: check, defined and convert coordinate system. 

- The first check coordinate, normally you must chose to "Properties" and go to metadata to check coordinate system. And once time, you must open and view a layer. With this plugin, you can check faster coordinate system all layer. They will print all information of layers. Especially, with Vietnam local coordinate system VN2000, this tool will print the name which the user often remember. 

- The second, for defined coordinate system, it's used to Vietnam Forest Map (VN2000 Noibo), it helps to defined CRS overlay with google map, satellite image, because VN2000 Noibo used 3 parameters so they don't overlay with GE. 

- Finally, convert coordinate system use to convert between coordinates, especially convert VN2000 noi bo (Vietnam) to WGS84 Latlong, UTM overlay with Google earth.
