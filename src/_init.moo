# Import the primitive Stunt package.

program $composed:import_package_from_file
  {filename} = args;
  server_log(tostr("importing package: ", filename));
  fh = -1;
  try
    fh = file_open(filename, "r-tn");
    data = file_read(fh, 1000000);
    file_close(fh);
    fh = -1;
    package = parse_json(data, "embedded-types");
    object = $composed:import(package);
    $composed:install(object);
  finally
    fh > -1 && file_close(fh);
  endtry
.

;$composed:import_package_from_file("primitive-0.0.4.json")
