package com.tts.statusrelay.data;

import com.tts.util.data.Pair;
import com.tts.util.data.StringOperations;
import com.tts.util.data.Validation;
import com.tts.util.data.XmlDocument;
import com.tts.util.data.XmlNode;
import com.tts.util.gui.Versioning;
import com.tts.util.logging.Logger;
import com.tts.util.time.TimeOperations;
import java.nio.ByteOrder;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Iterator;
import org.apache.commons.codec.binary.Base64;
import org.apache.commons.lang3.ArrayUtils;

public class StatusRelayMessage {
    public static ByteOrder DefaultByteOrder;
    public static String DefaultServiceName;
    public static int DefaultBasePort;
    public static Versioning CurrentVersion;
    public Versioning Version = new Versioning();
    public long TSPackage = 0L;
    public HashMap<String, StatusRelayRegion> Regions = new HashMap();
    public String ErrorMsg = "";

    public StatusRelayMessage() {
    }

    public StatusRelayMessage(StatusRelayMessage src) {
        this.CopyFrom(src);
    }

    public void CopyFrom(StatusRelayMessage src) {
        this.Clear();
        if (src != null) {
            this.TSPackage = src.TSPackage;
            this.Version = src.Version;
            this.Regions = new HashMap(src.Regions);
            this.ErrorMsg = src.ErrorMsg;
        }
    }

    public void Update(StatusRelayMessage src) {
        if (src != null) {
            Iterator var2 = src.Regions.keySet().iterator();

            while(var2.hasNext()) {
                String srcReg = (String)var2.next();
                if (this.Regions.containsKey(srcReg)) {
                    ((StatusRelayRegion)this.Regions.get(srcReg)).Update((StatusRelayRegion)src.Regions.get(srcReg));
                } else {
                    this.Regions.put(srcReg, src.Regions.get(srcReg));
                }
            }

        }
    }

    public StatusRelayMessage GetMessageWithSpecificRegion(String region) {
        StatusRelayMessage rv = new StatusRelayMessage();
        if (region.isEmpty()) {
            return rv;
        } else {
            rv.TSPackage = this.TSPackage;
            rv.Version = this.Version;
            Iterator var3 = this.Regions.keySet().iterator();

            while(var3.hasNext()) {
                String statusRegion = (String)var3.next();
                if (statusRegion == region) {
                    rv.Regions.put(statusRegion, this.Regions.get(statusRegion));
                    break;
                }
            }

            rv.ErrorMsg = this.ErrorMsg;
            return rv;
        }
    }

    public void Clear() {
        this.Clear(true);
    }

    public void Clear(Boolean complete) {
        if (complete) {
            this.Version = new Versioning();
        }

        this.TSPackage = 0L;
        this.Regions.clear();
        this.ErrorMsg = "";
    }

    public String ToJSONString() {
        StringBuilder sb = new StringBuilder();
        sb.append("{");
        sb.append("\"ErrorMsg\":\"" + this.ErrorMsg + "\"");
        sb.append(",\"TSRequest\":\"").append(TimeOperations.GetTimeString(this.TSPackage)).append("\"");
        sb.append(",\"Regions\":");
        Iterator var2 = this.Regions.values().iterator();

        while(var2.hasNext()) {
            StatusRelayRegion region = (StatusRelayRegion)var2.next();
            sb.append(region.ToJSONString());
        }

        sb.append("}");
        return sb.toString();
    }

    public String ToXMLString(long tsPackage) {
        return this.ToXMLString(false, false, "", tsPackage);
    }

    public String ToXMLString(Boolean prettyPrint, Boolean includeHeader, String prefix, long tsPackage) {
        String x2 = prettyPrint ? prefix : "";
        String p2 = prettyPrint ? prefix + StringOperations.SkinnyIndentation : "";
        String h2 = prettyPrint ? "\n" : "";
        StringBuilder sb = new StringBuilder();
        if (includeHeader) {
            sb.append(x2 + "<" + this.getClass().getName() + ">");
        }

        sb.append(h2 + p2 + "<Version>" + CurrentVersion.toString() + "</Version>");
        this.TSPackage = TimeOperations.GetCurrentTime();
        sb.append(h2 + p2 + "<TSPackage>" + TimeOperations.GetTimeUTC(tsPackage) + "</TSPackage>");
        sb.append(h2 + p2 + "<Regions>" + ToEncodedString(this.Regions) + "</Regions>");
        sb.append(h2 + p2 + "<ErrorMsg>" + this.ErrorMsg + "</ErrorMsg>");
        if (includeHeader) {
            sb.append(h2 + x2 + "</" + this.getClass().getName() + ">");
        }

        return sb.toString();
    }

    public static String ToEncodedString(HashMap<String, StatusRelayRegion> Regions) {
        String rv = "";
        ArrayList<Byte> bData = new ArrayList();
        bData.add((byte)Regions.size());
        Iterator var3 = Regions.keySet().iterator();

        while(var3.hasNext()) {
            String sVal = (String)var3.next();
            bData.addAll(Arrays.asList(((StatusRelayRegion)Regions.get(sVal)).ToByteArray(CurrentVersion)));
        }

        rv = Base64.encodeBase64String(ArrayUtils.toPrimitive((Byte[])bData.toArray(new Byte[bData.size()])));
        return rv;
    }

    public static StatusRelayMessage ParseXML(XmlNode src) {
        return ParseXML(src, (Logger)null);
    }

    public static StatusRelayMessage ParseXML(XmlNode src, Logger log) {
        if (src == null) {
            return null;
        } else {
            new Pair();
            new Pair();
            StatusRelayMessage rv = new StatusRelayMessage();
            XmlNode versionNode = src.SelectSingleNode("Version");
            if (versionNode != null) {
                Pair<Boolean, Versioning> tVer = Validation.ValidateVersionString(versionNode.InnerText.trim());
                if ((Boolean)tVer.Obj1) {
                    rv.Version.CopyFrom((Versioning)tVer.Obj2);
                }
            }

            XmlNode tsPackageNode = src.SelectSingleNode("TSPackage");
            if (tsPackageNode != null) {
                Pair<Boolean, Long> lVal = Validation.ValidateLongString(tsPackageNode.InnerText.trim());
                if ((Boolean)lVal.Obj1) {
                    rv.TSPackage = (Long)lVal.Obj2;
                }
            }

            XmlNode regionsNode = src.SelectSingleNode("Regions");
            if (regionsNode != null) {
                rv.Regions = ParseEncodedData(regionsNode.InnerText.trim(), rv.Version);
            }

            XmlNode errorNode = src.SelectSingleNode("ErrorMsg");
            if (errorNode != null) {
                rv.ErrorMsg = errorNode.InnerText.trim();
            }

            return rv;
        }
    }

    public static StatusRelayMessage ParseXMLString(String src) {
        return ParseXMLString(src, (Logger)null);
    }

    public static StatusRelayMessage ParseXMLString(String src, Logger log) {
        StatusRelayMessage rv = null;

        try {
            XmlDocument xDoc = new XmlDocument();
            xDoc.LoadXml(src);
            XmlNode rootNode = xDoc.SelectSingleNode(StatusRelayMessage.class.getSimpleName());
            if (rootNode == null) {
                throw new Exception("root node '" + StatusRelayMessage.class.getSimpleName() + "' could not be found");
            }

            rv = ParseXML(rootNode, log);
        } catch (Exception var5) {
            if (log != null) {
                log.Print("ERROR in " + StatusRelayMessage.class.getSimpleName() + "::ParseXMLString() -- " + var5.getMessage());
            }

            rv = null;
        }

        return rv;
    }

    public static HashMap<String, StatusRelayRegion> ParseEncodedData(String src, Versioning v) {
        return ParseEncodedData(src, v, (Logger)null);
    }

    public static HashMap<String, StatusRelayRegion> ParseEncodedData(String src, Versioning v, Logger log) {
        HashMap rv = new HashMap();

        try {
            int offset = 0;
            Byte[] bData = ArrayUtils.toObject(Base64.decodeBase64(src));
            Pair<Integer, StatusRelayRegion> tRegion = null;
            int regionCount = bData[offset];
            int offset = offset + 1;

            for(int i = 0; i < regionCount; ++i) {
                tRegion = StatusRelayRegion.ParseByteArray(bData, v, offset);
                offset = (Integer)tRegion.Obj1;
                if (tRegion.Obj2 == null) {
                    throw new Exception("Failure to parse region");
                }

                if (rv.containsKey(((StatusRelayRegion)tRegion.Obj2).RegionName)) {
                    ((StatusRelayRegion)rv.get(((StatusRelayRegion)tRegion.Obj2).RegionName)).Update((StatusRelayRegion)tRegion.Obj2);
                } else {
                    rv.put(((StatusRelayRegion)tRegion.Obj2).RegionName, tRegion.Obj2);
                }
            }

            return rv;
        } catch (Exception var9) {
            if (log != null) {
                log.Print("ERROR in StatusRelayRegion::ParseEncodedData() -- " + var9.getMessage());
            }

            return null;
        }
    }

    static {
        DefaultByteOrder = ByteOrder.LITTLE_ENDIAN;
        DefaultServiceName = "PostStatus";
        DefaultBasePort = 6711;
        CurrentVersion = new Versioning("1, 0, 0");
    }
}
