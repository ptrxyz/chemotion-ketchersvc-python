from helper import ConfigProps, Configuration

myProps = ConfigProps.from_env(prefix="CONFIG_")
myconfig = Configuration(myProps)
