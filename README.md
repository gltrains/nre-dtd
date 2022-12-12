# nre-dtd
A tool for downloading data from the National Rail Enquiries' data feed.

This code is licensed under the WTFPL or the CC0 (at your discretion), but its output is not. Any NRE data included in the output of this program is subject to these [terms and conditions](https://opendata.nationalrail.co.uk/terms).

## Useful links
- [DTD](https://wiki.openraildata.com/index.php?title=DTD) on the Open Rail Data Wiki
- [Fares and Associated Data Feed Interface Specification](https://www.raildeliverygroup.com/files/Publications/services/rsp/RSPS504502-00FaresandAssociatedDataFeedInterfaceSpecification.pdf) by the Rail Delivery Group
- [National Routeing Guide Data Feed Specification](https://www.raildeliverygroup.com/files/Publications/services/rsp/RSPS504702-00NationalRoutingGuideDataFeedSpecification.pdf) by the Rail Delivery Group
- [Timetable Information Data Feed Interface Specification](https://www.raildeliverygroup.com/files/Publications/services/rsp/RSPS5046_timetable_information_data_feed_interface_specification.pdf) by the Rail Delivery Group
- [How to use the National Routeing Guide](http://datafeeds.rdg.s3.amazonaws.com/RSPS5047/nrg_instructions.pdf) by the Rail Delivery Group (not HTTPS)
- [The National Routeing Guide in detail](http://datafeeds.rdg.s3.amazonaws.com/RSPS5047/nrg_detail.pdf) by the Rail Delivery Group (not HTTPS)

## Get started
### Get an account
- Register for an account on the [National Rail Data Portal](https://opendata.nationalrail.co.uk/).
- Subscribe to the Fares, Routeing and Timetable feed.

### Use the tool
#### From PyPI
- Run `python3 -m pip install nre-dtd`.
#### From source
- Run `python3 -m pip install poetry` if you have not got Poetry.
- Run `poetry init` to set up the environment.
- Run `poetry shell` to enter the environment.
- Or, prepend `poetry run --` to every command.

### Examples
#### Get usage instructions
```sh
nre-dtd --help
```

### Download everything
```sh
nre-dtd --fares <filename>.zip --routeing <filename>.zip --timetable <filename>.zip
```
This will ask you for a password. The downloaded files are zipped.

### Supply the username and password on the command line
```sh
nre-dtd --username sarah@example.com --password "correct-horse-battery-staple" <...>
```

![Powered by National Rail Enquiries](powered_by_nre.png)