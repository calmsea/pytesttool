<?xml version="1.0" encoding="UTF-8" ?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
<xsl:output
    method="html"
    doctype-public="-//W3C//DTD XHTML 1.0 Strict//EN"
    doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd" />

<xsl:variable name="testinfocolspan" select="4"/>
<xsl:variable name="reportcolspan" select="4"/>
<xsl:template match="/">
  <html>
    <head>
      <style>
        .script {margin:0; padding-left:1em; padding-bottom:1ex}
      </style>
    </head>
    <body>
      <table border="1" cellpadding="4">
        <thead>
          <tr>
            <th colspan="{$testinfocolspan}">項目</th>
          </tr>
          <tr>
            <th>No</th>
            <th>Title</th>
            <th>Description</th>
            <th>手順</th>
          </tr>
        </thead>
        <tbody>
          <xsl:for-each select="autotest/tests">
            <xsl:apply-templates select="tests/test"/>
          </xsl:for-each>
        </tbody>
      </table>
    </body>
  </html>
</xsl:template>

<xsl:template match="tester">
  <xsl:value-of select="name"/>
</xsl:template>

<xsl:template match="test">
  <xsl:if test="(count(reports/report)=0) and (count(test)=0)">
    <tr>
      <td><xsl:value-of select="@id"/></td>
      <td><xsl:value-of select="title"/></td>
      <td><xsl:value-of select="description"/></td>
      <td><xsl:apply-templates select="procedure"/></td>
    </tr>
  </xsl:if>
</xsl:template>

<xsl:template match="procedure">
  <div class="initialize">
    <b>初期化：</b>
    <xsl:apply-templates select="initialize"/>
  </div>
  <div class="main">
    <b>試験：</b>
    <xsl:apply-templates select="main"/>
  </div>
  <div class="finalize">
    <b>後処理：</b>
    <xsl:apply-templates select="finalize"/>
  </div>
</xsl:template>

<xsl:template match="initialize|main|finalize">
  <xsl:if test="count(script)=0">
    <p class="script">None</p>
  </xsl:if>
  <xsl:apply-templates select="script"/>
</xsl:template>

<xsl:template match="script">
  <p style="margin:0"><b>[
  <xsl:if test="@protocol"><xsl:value-of select="@protocol"/>://</xsl:if>
  <xsl:if test="@user"><xsl:value-of select="@user"/></xsl:if>
  <xsl:if test="@passwd">:<xsl:value-of select="@passwd"/></xsl:if>
  <xsl:if test="@host">@<xsl:value-of select="@host"/></xsl:if>
  ]</b></p>
  <pre class="script">
    <code><xsl:value-of select="."/></code>
  </pre>
</xsl:template>

<xsl:template match="log">
  <xsl:for-each select="*">
    <xsl:variable name="name" select="name()"/>
    <b><xsl:value-of select="$name"/></b>
    <pre class="log"><xsl:value-of select="."/></pre>
  </xsl:for-each>
</xsl:template>

</xsl:stylesheet>
