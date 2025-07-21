PPI Specification v0.1.1 

IOWarp is in active development, and the architecture laid out in this document is not fully implemented at this time.

= Overview 

The Platform Plugin Interface (PPI) is a module within the IOWarp platform that enables user-developed plugins to extend existing platform capabilities and introduce new functionality. The PPI serves as a standardized interface layer, primarily designed for consumption by AI agents while remaining accessible to human developers and automated scripts. 

= Plugin Architecture 

== Plugin Structure 

A PPI plugin consists of a collection of files in a subfolder in the same directory as the Warp executable.  Each plugin must contain: 

    plugin.yaml - Plugin metadata file consumed by the IOWarp agent. See ‘Plugin Specification’ for further details 

    Executable or script file referenced by by ‘server_path’ within the plugin.yaml file to launch the MCP server 

Optional Files: 

    Plugin-specific configuration files 

    Resource files and assets 

    Additional modules or dependencies 

    Installation/build instructions 

== Plugin Specification 

    name: name of the plugin 

    description: natural-language description of the plugin’s broad purpose and capabilities 

    server_path – Relative path to the executable/script to start the MCP server 

== Plugin Detection 

A plugin is considered to be installed and available by the IOWarp agent when  

    The plugin subfolder contains a valid plugin.yaml file with all required fields 

    The executable/script file exists at the specified server_path 

== Plugin Lifecycle 

In the contest of IOWarp as a whole, the standard plugin execution flow shall follow these steps: 

    User submits a request to central IOWarp agent 

    IOWarp agent queries built-in module capabilities first (CAE, CTE, etc). If no built-in module can satisfy the request, or if explicitly requested by the user, the agent evaluates installed plugins by examining their plugin.yaml descriptions. 

    For each plugin that appears relevant to the user’s request, the IOWarp agent will request a list of the candidate plugin’s exposed tools. 

    If the agent determines that one or more plugins should be used in order to satisfy the user request, the agent will start the respective MCP server(s). 

    The agent makes the necessary tool call(s) to the local MCP server(s). 

    The agent either terminates the server(s) and connection(s) or keeps both alive to optimize for potential repeated usage. 

 

While use of the MCP protocol introduces some complexity by requiring IOWarp to manage servers locally, the benefits of interfacing with plugins written in different languages internally, as well as the benefit of conforming to a popular standard, are considered to outweigh this cost. 

 

== TBD: Remote MCP Support 

Since PPI plugin usage fundamentally wraps MCP calls, the architecture naturally lends itself towards supporting integration with remote MCP servers. This would include both public facing externally developed remote MCP servers, as well as “internal” remote MCP servers, hosted by IOWarp or the PPI itself and exposed only to other distributed nodes of the runtime. 

This capability would offer value for distributed deployments where many IOWarp nodes require access to the same plugin functionality. 

This would require the following changes to the architecture: 

    Addition of an optional “type” field to plugin.yaml that is either “remote” or “local”, defaulting to “local”, as well as a second field for “external” or “internal” remote MCPs. 

    Potentially, the addition of a “trust level” optional field to the plugin.yaml. This would determine what kinds of information the agent would be willing to send over the remote connection for the case of “external” remote MCPs. This would primarily be useful if automatic remote MCP discovery is added, as otherwise it makes the most sense to assume the user trusts remote MCPs they choose to use. 

    Connection-specific information for “internal” remote MCPs. 

    Plugins designated as “remote” will need to replace the server executable with a “proxy server” executable that forwards requests to the remote MCP endpoints using a user/agent-configured connection, API keys, etc. 