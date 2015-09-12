#
# Example python script to generate a BOM from a KiCad generic netlist
#
# Example: Sorted and Grouped CSV BOM
#

"""
    @package
    Generate a Tab delimited list (csv file type).
    Components are sorted by ref and grouped by value with same footprint.
    A number of different BOMs are generated (identified by suffix).
    The following suppliers are considered when looking up parts:
    'Mouser', 'Farnell', 'Elfa', 'Digi-Key', 'AliExpress', 'eBay', 'RS'.
    In addition to this, if the suppliers are sorted by price, with the cheapest
    alternative as the "primary" supplier (Supplier1), the suffix 'Cheapest' contains a BOM
    with potentially mixed suppliers, but the cheapest alternative for each part.
    This also gurantees that every component is included (since some components may
    not be available from a specific supplier).
    The suffix 'Full' indicate a full BOM table with all available suppliers listed.
    The supplier-specific BOMs vary slightly in formatting due to supplier specific
    requirement for import data formats.
"""

# Import the KiCad python helper module and the csv formatter
import kicad_netlist_reader
import csv
import sys
import re

def natural_sort(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower() 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(l, key = alphanum_key)

# Generate an instance of a generic netlist, and load the netlist tree from
# the command line option. If the file doesn't exist, execution will stop
net = kicad_netlist_reader.netlist(sys.argv[1])

# List the outputs we plan to generate
supplier_list = ["Full", "Cheapest", "Mouser", "Farnell", "Elfa", "Digi-Key", "AliExpress", "eBay", "RS"]

for supplier in supplier_list:

  # Open a file to write to, if the file cannot be opened output to stdout
  # instead
  try:
    if supplier == "Mouser":
      f = open(sys.argv[2]+"_"+supplier+".csv", 'w')
    else:
      f = open(sys.argv[2]+"_"+supplier+".txt", 'w')
  except IOError:
    e = "Can't open output file for writing: " + sys.argv[2]
    print(__file__, ":", e, sys.stderr)
    f = sys.stdout

  # Create a new csv writer object to use as the output formatter
  if supplier == "Mouser":
    out = csv.writer(f, lineterminator='\n', delimiter=',', quotechar='\"', quoting=csv.QUOTE_MINIMAL)
  else:
    out = csv.writer(f, lineterminator='\n', delimiter='\t', quotechar='\"', quoting=csv.QUOTE_MINIMAL)

  # Output a set of rows for a header providing general information
  if supplier == "Elfa":
    out.writerow(['Supplier part', 'Count', 'Reference'])
  elif supplier == "Digi-Key":
    out.writerow([])
  elif supplier == "Full":
    out.writerow(['Count', 'Reference', 'Value', 'Footprint', 'Datasheet', 'Vendor', 'Vendor part', 'Supplier1', 'Supplier1 part', 'Supplier1 link', 'Supplier2', 'Supplier2 part', 'Supplier2 link', 'Supplier3', 'Supplier3 part', 'Supplier3 link', 'Supplier4', 'Supplier4 part', 'Supplier4 link', 'Supplier5', 'Supplier5 part', 'Supplier5 link'])
  else:
    out.writerow(['Count', 'Reference', 'Value', 'Footprint', 'Datasheet', 'Vendor', 'Vendor part', 'Supplier', 'Supplier part', 'Supplier link'])


  # Get all of the components in groups of matching parts + values
  # (see kicad_netlist_reader.py)
  grouped = net.groupComponents()

  # Output all of the component information
  for group in grouped:
    refs = ""

    for component in group:
      refs += component.getRef() + " "
      c = component
    refs = refs[:-1]
    ref_list = refs.split(' ')
    ref_list = natural_sort(ref_list)
    refs = " ".join(ref_list)
    
    if supplier == "Cheapest":
      cur_supplier = net.getGroupField(group, "Supplier1")
      cur_part = net.getGroupField(group, "Supplier1 part")
      cur_link = net.getGroupField(group, "Supplier1 link")
    else:
      if net.getGroupField(group, "Supplier1") == supplier:
        cur_supplier = net.getGroupField(group, "Supplier1")
        cur_part = net.getGroupField(group, "Supplier1 part")
        cur_link = net.getGroupField(group, "Supplier1 link")
      elif net.getGroupField(group, "Supplier2") == supplier:
        cur_supplier = net.getGroupField(group, "Supplier2")
        cur_part = net.getGroupField(group, "Supplier2 part")
        cur_link = net.getGroupField(group, "Supplier2 link")
      elif net.getGroupField(group, "Supplier3") == supplier:
        cur_supplier = net.getGroupField(group, "Supplier3")
        cur_part = net.getGroupField(group, "Supplier3 part")
        cur_link = net.getGroupField(group, "Supplier3 link")
      elif net.getGroupField(group, "Supplier4") == supplier:
        cur_supplier = net.getGroupField(group, "Supplier4")
        cur_part = net.getGroupField(group, "Supplier4 part")
        cur_link = net.getGroupField(group, "Supplier4 link")
      elif net.getGroupField(group, "Supplier5") == supplier:
        cur_supplier = net.getGroupField(group, "Supplier5")
        cur_part = net.getGroupField(group, "Supplier5 part")
        cur_link = net.getGroupField(group, "Supplier5 link")
      else:
        cur_supplier = "Missing"
        cur_part = "Missing"
        cur_link = "Missing"

    # Fill in the component groups common data (some vendors have specific requirements
    if supplier == "Elfa":
      out.writerow([cur_part, len(group), refs])
    elif supplier == "Digi-Key":
      out.writerow([len(group), cur_part, refs])
    elif supplier == "Full":
      out.writerow([len(group), refs, c.getValue(), net.getGroupFootprint(group), net.getGroupDatasheet(group),
        net.getGroupField(group, "Vendor"), net.getGroupField(group, "Vendor part"),
	net.getGroupField(group, "Supplier1"), net.getGroupField(group, "Supplier1 part"), net.getGroupField(group, "Supplier1 link"),
	net.getGroupField(group, "Supplier2"), net.getGroupField(group, "Supplier2 part"), net.getGroupField(group, "Supplier2 link"),
	net.getGroupField(group, "Supplier3"), net.getGroupField(group, "Supplier3 part"), net.getGroupField(group, "Supplier3 link"),
	net.getGroupField(group, "Supplier4"), net.getGroupField(group, "Supplier4 part"), net.getGroupField(group, "Supplier4 link"),
	net.getGroupField(group, "Supplier5"), net.getGroupField(group, "Supplier5 part"), net.getGroupField(group, "Supplier5 link")])
    else:
      out.writerow([len(group), refs, c.getValue(), net.getGroupFootprint(group), net.getGroupDatasheet(group),
        net.getGroupField(group, "Vendor"), net.getGroupField(group, "Vendor part"), cur_supplier, cur_part, cur_link])

