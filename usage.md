Usage:

jira (-a|--action) <action> [(-f|--file) <file>] [--encoding <encoding>] [--debug] [-v|--verbose] [--quiet] [--outputFormat

<outputFormat>] [--sql <sql>] [--driver <driver>] [--url <url>] [--host <host>] [--port <port>] [--database <database>] [--dbUser

<dbUser>] [--dbPassword <dbPassword>] [--propertyFile <propertyFile>] [--common <common>] [--findReplace <findReplace>]

[--findReplaceRegex <findReplaceRegex>] [--continue] [--simulate] (-s|--server) <server> (-u|--user) <user> (-p|--password)

<password> [--login <login>] [--service <service>] [-l|--loginFromStandardInput] [--project <project>] [--toProject <toProject>]

[--name <name>] [--description <description>] [--lead <lead>] [--after <after>] [--issue <issue>] [--toIssue <toIssue>] [--parent

<parent>] [--summary <summary>] [--priority <priority>] [--reporter <reporter>] [--assignee <assignee>] [--security <security>]

[--environment <environment>] [--component <component>] [--toComponent <toComponent>] [--components <components>] [--version

<version>] [--affectsVersions <affectsVersions>] [--fixVersions <fixVersions>] [--custom <custom>] [--field <field>] [--field2

<field2>] [--fieldExcludes <fieldExcludes>] [--date <date>] [--dateFormat <dateFormat>] [--type <type>] [--resolution <resolution>]

[--labels <labels>] [--step <step>] [--comment <comment>] [--filter <filter>] [--search <search>] [--link <link>] [--values

<values>] [--values2 <values2>] [--timeSpent <timeSpent>] [--estimate <estimate>] [--id <id>] [--propertyPrefix <propertyPrefix>]

[--jsp <jsp>] [--request <request>] [--requestParameters <requestParameters>] [--count <count>] [--api <api>] [--plugin <plugin>]

[--role <role>] [--group <group>] [--defaultGroup <defaultGroup>] [--userId <userId>] [--userFullName <userFullName>] [--userEmail

<userEmail>] [--userPassword <userPassword>] [--permissionScheme <permissionScheme>] [--notificationScheme <notificationScheme>]

[--issueSecurityScheme <issueSecurityScheme>] [--workflowScheme <workflowScheme>] [--issueTypeScheme <issueTypeScheme>]

[--fieldConfigurationScheme <fieldConfigurationScheme>] [--autoVersion] [--autoComponent] [--autoGroup] [--autoAdjust] [--asVersion]

[--asComponent] [--asCascadeSelect] [--append] [--appendText] [--copyLinks] [--copyAttachments] [--copyComments] [--copyWatchers]

[--copySubtasks] [--copySubtaskEstimates] [--useParentVersions] [--cloneIssues] [--copyVersions] [--copyComponents]

[--copyRoleActors] [--replace] [--help]



Provides capability to make requests to a remote server.

Required parameters: action, server, password.

Optional parameters: user (likely required for your installation).

Other required and optional parameters depending on action requested.



(-a|--action) <action>

      Requested operation to perform. Valid actions (not case sensitive) are:

      

      login - Login to remote server. Returns login token.

       Required parameters: password

       Optional parameters: user

      logout - Logout of remote server.

      run - Run script from a file or standard input.

       Required parameters: file

       Optional parameters: common, continue, simulate, encoding, findReplace

      runFromSql - Run script generated.by SQL provided by the sql parameter, a file, or standard input

       Required parameters: sql or file or standard input

       Optional parameters: common, host, driver, database, host, port, url, dbUser, dbPassword,

       propertyFile, continue, simulate, encoding, findReplace

      runFromCsv - Run script generated from a CSV file.

       Required parameters: file

       Optional parameters: common, propertyFile, continue, quiet, simulate, encoding, findReplace

      runFromIssueList - Run actions for each issue from an issue list based on a filter or a search.

       Required parameters: filter or search

       Optional parameters: common, continue, simulate, count, file, encoding, findReplace

      getClientInfo - Get information about the this client tool.

      getServerInfo - Get information about the JIRA server.

      renderRequest - Render url based request.

       Required parameters: request

       Optional parameters: requestParameters, issue, file, encoding

      getCustomFieldList - Get information on all custom fields.

      createProject - Create a new project with key provided by project parameter.

       Required parameters: project, lead

       Optional parameters: name, description, url, permissionScheme, notificationScheme, issueSecurityScheme, workflowScheme,

       issueTypeScheme, fieldConfigurationScheme

      updateProject - Update project information.

       Required parameters: project

       Optional parameters: name, description, lead, url,

       permissionScheme, notificationScheme, issueSecurityScheme, workflowScheme,

       issueTypeScheme, fieldConfigurationScheme

      cloneProject - Create a new project as a clone of a base project. Optionally copy versions, components, role actors,

       and issues to new project.

       Issue cloning requires JIRA Clone Plus Plugin.

       Required parameters: project, toProject

       Optional parameters: name, description, url, permissionScheme, notificationScheme, issueSecurityScheme,

       search, type, continue, copyVersions, copyComponents, copyRoleActors, cloneIssues,

       copyLinks, copyAttachments, copyComments, copyWatchers, copySubtasks, copySubtaskEstimates, useParentVersions,

       fieldExcludes, propertyPrefix, jsp

      deleteProject - Delete a project.

       Required parameters: project

      getProject - Get project information.

       Required parameters: project

       Optional parameters: file, encoding

      getProjectList - List defined projects.

       Optional parameters: outputFormat, file, encoding

       Output formats: 1 - default, 2 - scheme info

      getVersion - Get information for a project version (since JIRA 4.2).

       Required parameters: project, version

       Optional parameters: dateFormat, file, encoding

      addVersion - Add a new version to a project.

       Required parameters: project, version

       Optional parameters: after, date, dateFormat, replace

      updateVersion - Update version for a project.

       Required parameters: project, version

       Optional parameters: name, description, after, date, dateFormat, autoVersion, api

      copyVersion - Copy a version from one project to the same project or another project.

       Required parameters: project, version

       Optional parameters: toProject, name, after, date, dateFormat, replace

      copyVersions - Copy all versions from one project to another project.

       Required parameters: project, toProject

       Optional parameters: continue, replace

      deleteVersion - Delete a version from a project. Update affects and fix versions for issues by removing version reference

       or swapping it with versions specified.

       Required parameters: project, version

       Optional parameters: affectsVersions, fixVersions, autoVersion, api

      releaseVersion - Release a version for a project. Resets release date if provided. Defaults to current if release date

       is not set.

       Required parameters: project, version

       Optional parameters: date, dateFormat

      unreleaseVersion - Unrelease a version for a project, optionally reset release date.

       Required parameters: project, version

       Optional parameters: date, dateFormat

      archiveVersion - Archive a version for a project. This hides the version from the UI.

       Required parameters: project, version

      unarchiveVersion - Unarchive a version for a project. This makes the version visible again in the UI.

       Required parameters: project, version

      getComponent - Get information for a component of a project (since JIRA 4.2).

       Required parameters: project, component

       Optional parameters: file, encoding, api

      addComponent - Add component to a project.

       Required parameters: project, component

       Optional parameters: description, lead, replace, api

      updateComponent - Update component for a project (since JIRA 4.4).

       Required parameters: project, component

       Optional parameters: name, description, lead, api

      deleteComponent - Delete component from a project.

       Required parameters: project, component

       Optional parameters: api

      copyComponent - Copy a component from one project to the same project or another project (since JIRA 4.2).

       Required parameters: project, component

       Optional parameters: toProject, name, description, lead, replace, api

      copyComponents - Copy all or some components from one project to another.

       Required parameters: project, toProject

       Optional parameters: components, replace, api

      getVersionList - List versions defined for a projects.

       Required parameters: project

       Optional parameters: file, encoding

      getComponentList - List components defined for a projects.

       Required parameters: project

       Optional parameters: file, encoding

      getSecurityLevelList - List security levels defined for a projects.

       Required parameters: project

       Optional parameters: file, encoding

      getProjectRoleList - Get project roles.

      getProjectRoleActorList - Get users and groups for a project's role.

       Required parameters: project, role

      addProjectRoleActors - Add users or groups to a project role.

       Required parameters: project, role, userId or group

      copyProjectRoleActors - Copy all role actors from a project to another project.

       Required parameters: project, toProject

       Optional parameters: continue

      removeProjectRoleActors - Remove users or groups from a project role.

       Required parameters: project, role, userId or group

      createIssue - Create a new issue for a project.

       Required parameters: project, type, summary

       Optional parameters: priority, reporter, assignee, description, components, affectsVersions, fixVersions, environment,

       security, field, values, field2, values2, asVersion, asComponent, asCascadeSelect,

       date, dateFormat, custom, autoVersion, autoComponent, comment, group, role, findReplace, file, encoding

      deleteIssue - Delete an issue.

       Required parameters: issue

      cloneIssue - Create a new issue by copying an existing issue.

       Required parameters: issue

       Optional parameters: type, summary, resolution, labels,

       comment, group, rolepriority, reporter, assignee, description, components, affectsVersions, fixVersions, environment,

       security, field, values, field2, values2, asVersion, asComponent, asCascadeSelect,

       date, dateFormat, custom, autoVersion, autoComponent, , findReplace, file, encoding

       project, copyLinks, copyAttachments, copyComments, copyWatchers, copySubtasks, copySubtaskEstimates, useParentVersions,

       fieldExcludes, propertyPrefix, jsp

      cloneIssues - Clone issues returned from a JQL search.

       Required parameters: search

       Optional parameters: project, type, continue,

       copyLinks, copyAttachments, copyComments, copyWatchers, copySubtasks, copySubtaskEstimates, useParentVersions,

       autoVersion, autoComponent, fieldExcludes, propertyPrefix, jsp

      updateIssue - Update an existing issue.

       Required parameters: issue

       Optional parameters: type, summary, resolution, labels,

       priority, reporter, assignee, description, components, affectsVersions, fixVersions, environment,

       security, field, values, field2, values2, asVersion, asComponent, asCascadeSelect,

       date, dateFormat, custom, autoVersion, autoComponent, , append, appendText, comment, group, role, findReplace, file,

      encoding

      progressIssue - Progress issue through workflow.

       Required parameters: issue, step

       Optional parameters: type, summary, resolution, labels,

       priority, reporter, assignee, description, components, affectsVersions, fixVersions, environment,

       security, field, values, field2, values2, asVersion, asComponent, asCascadeSelect,

       date, dateFormat, custom, autoVersion, autoComponent, comment, group, role, findReplace, file, encoding

      addComment - Add a comment to an issue.

       Required parameters: issue

       Optional parameters: comment, group, role, findReplace, file, encoding

      addAttachment - Add an attachment to an issue.

       Required parameters: issue, file

       Optional parameters: findReplace, name, encoding

      getIssue - Get information about an existing issue.

       Required parameters: issue

       Optional parameters: file, dateFormat, asVersion, encoding

      getFieldValue - Get field value for an issue.

       Required parameters: issue, field

       Optional parameters: file, dateFormat, asVersion, encoding

      setFieldValue - Set custom field value for an issue.

       Required parameters: issue, field, file or values

       Optional parameters: field2, values2, asVersion, asComponent, asCascadeSelect, append, appendText, encoding, dateFormat

      getAvailableSteps - Get available workflow steps for issue.

       Required parameters: issue

       Optional parameters: file, encoding

      addLabels - Add labels to an issue.

       Required parameters: issue, labels

      removeLabels - Remove labels from an issue.

       Required parameters: issue, labels

      addWatchers - Add watchers to an issue.

       Required parameters: issue

       Optional parameters: userId

      removeWatchers - Remove watchers from an issue.

       Required parameters: issue

       Optional parameters: userId

      addWork - Add work log entry.

       Required parameters: issue, timeSpent

       Optional parameters: comment, date, dateFormat, estimate, role, group, autoAdjust

      removeWork - Remove work log entry.

       Required parameters: id

      updateWork - Update work log entry.

       Required parameters: id, issue

       Optional parameters: timeSpent, comment, date, dateFormat, estimate, role, group, autoAdjust

      getWorkList - Get list of a work log entry.

       Required parameters: issue

       Optional parameters: dateFormat, file, encoding

      linkIssue - Link an issue to another issue.

       Required parameters: issue, toIssue, link

       Optional parameters: comment

      deleteLink - Remove link to another issue.
       Required parameters: issue, toIssue, link
      getIssueList - List issues for a filter or a search.
       Required parameters: filter or search
       Optional parameters: file, dateFormat, count, outputFormat, encoding
       Output formats: 1 - default, 2 or 4 - custom fields, 3 or 4 - security level, 5 - 4 plus time values, 998 - all available
      fields except custom, 999 - all available fields
      getCommentList - List of comment information (id, dates, ...) for an issue.
       Required parameters: issue
       Optional parameters: file, dateFormat, encoding
      getComments - Get a formatted string of all comment text for an issue.
       Required parameters: issue
       Optional parameters: file, dateFormat, encoding
      getAttachment - Get lastest attachment by name or id for an issue.
       Required parameters: issue, file
       Optional parameters: name, encoding
      getAttachmentList - List all attachments for an issue.
       Required parameters: issue, file
       Optional parameters: dateFormat, encoding
      getUser - Get user information. JIRA 4.2 or higher.
       Required parameters: userId
       Optional parameters: file, endcoding
      addUser - Add a new user.
       Required parameters: userId, userEmail
       Optional parameters: userFullName, userPassword
      addUserWithFile - Add users from comma separated file.
       Required parameters: file
       Optional parameters: encoding
      updateUser - Update user information.
       Required parameters: userId
       Optional parameters: userFullName, userEmail
      removeUser - Remove a user.
       Required parameters: userId
      removeUserWithFile - Remove users from comma separate file.
       Required parameters: file
       Optional parameters: encoding
      addGroup - Add a new group.
       Required parameters: group
      removeGroup - Remove a group.
       Required parameters: group
       Optional parameters: defaultGroup
      addUserToGroup - Add user to a group.
       Required parameters: userId, group
       Optional parameters: autoGroup
      addUserToGroupWithFile - Add users to groups from comma separated file.
       Required parameters: file
       Optional parameters: autoGroup, encoding
      removeUserFromGroup - Remove user from a group.
       Required parameters: userId, group
      removeUserFromGroupWithFile - Remove users from groups from comma separated file.
       Required parameters: file
       Optional parameters: encoding
      getUserList - List users in a group.
       Required parameters: group
       Optional parameters: file, encoding
      getPluginList - Deprecated. Get list of plugins.
       Optional parameters: plugin, file, outputFormat, count
       Output formats: 1 - default, 2 - plugin exchange info
      getPluginDownload - Deprecated. Get url to download the plugin version. Version defaults to the latest version.
       Required parameters: plugin
       Optional parameters: version
[(-f|--file) <file>]
      Path to file based content or result output
[--encoding <encoding>]
      Character encoding (character set) for text based file content - must be an encoding supported by your JAVA platform.
[--debug]
      Requests detail debug output. Optional for all actions.
[-v|--verbose]
      Requests verbose output to help with problem determination. Optional for all actions.
[--quiet]
      Limit some output messages. Optional for all actions.
[--outputFormat <outputFormat>]
      Specify output format for an action. (default: 1)
[--sql <sql>]
      SQL select statement used to generate a run script.
[--driver <driver>]
      JDBC driver class or predefined value: postgresql, mysql, mssql, oracle, or db2400. Required for SQL actions.
[--url <url>]
      Action specific setting. Example: Database access url for SQL actions. Optional when host is provided.
[--host <host>]
      Database host server for SQL actions. Not used if url is provided. (default: localhost)
[--port <port>]
      Database host port for SQL actions. Optional, defaults to database default. Not used if url is provided.
[--database <database>]
      Database name is required for SQL actions.
[--dbUser <dbUser>]
      Database user name. Defaults to user.
[--dbPassword <dbPassword>]
      Database user password. Defaults to password.
[--propertyFile <propertyFile>]
      Property file with mapping information.
[--common <common>]
      Common parameter string added to all run actions.
[--findReplace <findReplace>]
      Find and replace text. Comma separated list of colon separated pairs. Single quote values containing a delimiter. Embedded
      quotes must be doubled.
[--findReplaceRegex <findReplaceRegex>]
      Find and replace text with a regular expression. Comma separated list of colon separated pairs. Single quote values
      containing a delimiter. Embedded quotes must be doubled.
[--continue]
      Continue processing even after errors are encountered.
[--simulate]
      Simulate running actions. Log the action that would be taken.
(-s|--server) <server>
      Server URL.
(-u|--user) <user>
      User name for remote login. (default: automation)
(-p|--password) <password>
      User password for remote login.
[--login <login>]
      Login token from previous login request.
[--service <service>]
      Service address extension. (default: /rpc/soap/jirasoapservice-v2)
[-l|--loginFromStandardInput]
      Get login token from standard input.
[--project <project>]
      Project name, key, or id
[--toProject <toProject>]
      Project name, key, or id to copy to
[--name <name>]
      Name
[--description <description>]
      Description
[--lead <lead>]
      Project lead user id
[--after <after>]
      Version name or id to add a version after. Defaults to after last version. Use -1 to make it the first version.
[--issue <issue>]
      Issue key or id
[--toIssue <toIssue>]
      Link destination issue key or id
[--parent <parent>]
      Parent issue key or id
[--summary <summary>]
      Summary of issue
[--priority <priority>]
      Issue priority - name or id
[--reporter <reporter>]
      Issue reporter user id
[--assignee <assignee>]
      Issue assignee user id
[--security <security>]
      Issue security level name or id
[--environment <environment>]
      Issue environment
[--component <component>]
      Project component name or id
[--toComponent <toComponent>]
      Project component name or id for JIRA 4.4 or higher
[--components <components>]
      Project components - comma separated names or ids
[--version <version>]
      Project version name or id or plugin version
[--affectsVersions <affectsVersions>]
      Affects versions - comma separated names or ids[--fixVersions <fixVersions>]
      Fix versions - comma separated names or ids
[--custom <custom>]
      Custom fields - comma separated key:value pairs. Key can be field name or id. Single quote the key:value pair if it contains
      a comma (,) or line breaks.
[--field <field>]
      Field name or id. For some actions, this parameter must be a custom field.
[--field2 <field2>]
      Field name or id for a custom field.
[--fieldExcludes <fieldExcludes>]
      Fields to exclude from cloning - comma separated list of fields.
[--date <date>]
      Date for version or due date for issue
[--dateFormat <dateFormat>]
      Format string for date in Java SimpleDateFormat, default is client date format.
[--type <type>]
      Issue type - name or id
[--resolution <resolution>]
      Resolution name or id
[--labels <labels>]
      Labels or tags. A blank separated list.
[--step <step>]
      Workflow step - name or id
[--comment <comment>]
      Comment for an issue
[--filter <filter>]
      Filter id or favorite filter name.
[--search <search>]
      Search JQL query.
[--link <link>]
      Link description. Examples: 'relates to' or 'is related to'. Link id can also be used for deleteLink.
[--values <values>]
      Comma separated list of field values
[--values2 <values2>]

      Comma separated list of field values
[--timeSpent <timeSpent>]
      Time spent on work using. Example: 3h 30m
[--estimate <estimate>]
      Estimate of time remaining for an issue. Example: 3h 30m
[--id <id>]
      Numeric id of an item.
[--propertyPrefix <propertyPrefix>]
      Prefix used for accessing properties for custom clone actions.
[--jsp <jsp>]
      Custom JSP name for clone actions
[--request <request>]
      URL fragment for a request.
[--requestParameters <requestParameters>]
      URL request parameters
[--count <count>]
      Maximum number of entries to return. (default: 2147483647)
[--api <api>]
      API version. Some requests produce different results based on the api version used. Use 0 for latest. (default: 0)
[--plugin <plugin>]
      Plugin key or partial key for matching.
[--role <role>]
      User role in project
[--group <group>]
      Group name
[--defaultGroup <defaultGroup>]
      Default group to move users on removeGroup action.
[--userId <userId>]
      User id for user management and other actions
[--userFullName <userFullName>]
      User name for user management actions
[--userEmail <userEmail>]
      User email for user management actions
[--userPassword <userPassword>]
      User password for user management actions
[--permissionScheme <permissionScheme>]
      Permission scheme name or id (default: Default Permission Scheme)
[--notificationScheme <notificationScheme>]
      Notification scheme name or id
[--issueSecurityScheme <issueSecurityScheme>]
      Issue security scheme name or id
[--workflowScheme <workflowScheme>]
      Workflow scheme name or id. Use blank for default scheme.
[--issueTypeScheme <issueTypeScheme>]
      Issue type scheme name or id. Use blank for default scheme.
[--fieldConfigurationScheme <fieldConfigurationScheme>]
      Field configuration scheme name or id. Use blank for default scheme.
[--autoVersion]

      Automatically add versions used in affectsVersions and fixVersions parameters.
[--autoComponent]
      Automatically add components used in components parameter.
[--autoGroup]
      Groups are automatically added when referenced in add user functions.
[--autoAdjust]
      Auto adjust remaining estimate when adding work entry.
[--asVersion]
      Interpret values parameter as version values and convert each to the version id.
[--asComponent]
      Interpret values parameter as component values and convert each to the component id.
[--asCascadeSelect]
      Interpret values parameter as a cascade select value ids.
[--append]
      Append values to existing values for version fields, components field, and custom fields supporting multiple values.
[--appendText]
      Append text to existing value text for description, environment, and single and multi-value custom fields.
[--copyLinks]
      Copy issue links when cloning an issue.
[--copyAttachments]
      Copy attachments when cloning an issue.
[--copyComments]
      Copy comments when cloning an issue.
[--copyWatchers]
      Copy Watchers when cloning an issue.
[--copySubtasks]
      Copy subtasks when cloning an issue.
[--copySubtaskEstimates]
      Copy subtask estimates when cloning an issue.
[--useParentVersions]
      Copy parent versions to subtask when cloning an issue.
[--cloneIssues]
      Clone issues when cloning a project.
[--copyVersions]
      Copy versions when cloning a project.
[--copyComponents]
      Copy components when cloning a project.
[--copyRoleActors]
      Copy project role actors when cloning a project.
[--replace]
      Replace existing entity.
[--help]
      Prints this help message.