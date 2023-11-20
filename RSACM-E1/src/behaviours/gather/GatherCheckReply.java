package behaviours.gather;

import behaviours.message.CheckMessage;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import jade.core.AID;
import jade.core.behaviours.Behaviour;
import jade.lang.acl.ACLMessage;
import jade.lang.acl.MessageTemplate;
import util.JadeUtil;

import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;
import java.util.concurrent.atomic.AtomicInteger;

public class GatherCheckReply extends Behaviour {
    private ArrayList<AID> repFunction;
    private Map<String, Integer> selectedAgg;
    private Map<StringBuilder, Integer> highQualityRep;
    private Map<StringBuilder, Integer> lowCostRep;
    private Map<String, Integer> highQualityRes;
    private Map<String, Integer> lowCostRes;
    public AtomicInteger serviceNum;
    private AtomicInteger andNum = new AtomicInteger(0);
    private AtomicInteger orNum = new AtomicInteger(0);
    private AtomicInteger addNum = new AtomicInteger(0);
    //    private Map<String, Integer> replaceMap = new HashMap<>();
    int step = 1;
    private int andRepliesCnt = 0;
    private int orRepliesCnt = 0;
    private int addRepliesCnt = 0;
    private int andRepliesNum = 0;
    private int orRepliesNum = 0;
    private int addRepliesNum = 0;
    private ACLMessage requireCheckMessage;
    int repliesCnt = 0;
    private AtomicInteger highQualityFunCapacity = new AtomicInteger(0);
    private AtomicInteger lowCostFunCapacity = new AtomicInteger(0);
    //    private AtomicBoolean latestFlag;
    private ArrayList<String> failedNei;
    private ArrayList<String> availableNei;
    private String orFailedFun;
    private String addFailedFun;
    private static Map<String, Set<String>> replaceView = null;
    static Map<String, ArrayList<String>> replacementMap;
    ObjectMapper mapper = new ObjectMapper();
    public static Map<String, Integer> updatedFunctions;
    boolean updated = false;
    String checkID;
    int noiseRate;
    public GatherCheckReply(int[] nums, AtomicInteger serviceNum, ACLMessage checkMsg,
            Map<String, Integer> selectedAgg, Map[] functions, ArrayList<AID> repFunction, Map[] resources,
            ArrayList<String> failedNei, ArrayList<String> availableNei, Map<String, Set<String>> replaceView,
            Map<String, ArrayList<String>> replacementMap, Map<String, Integer> updatedFunctions,int noiseRate) {
        this.andRepliesNum = nums[0];
        this.orRepliesNum = nums[1];
        this.addRepliesNum = nums[2];
//        this.replaceRepliesNum = num[2];
        this.serviceNum = serviceNum;
        this.requireCheckMessage = checkMsg;
        this.selectedAgg = selectedAgg;
        this.repFunction = repFunction;
        this.highQualityRep = functions[0];
        this.lowCostRep = functions[1];
        this.highQualityRes = resources[0];
        this.lowCostRes = resources[1];
//        this.latestFlag = latestFlag;
        this.failedNei = failedNei;
        this.availableNei = availableNei;
        this.replaceView = replaceView;
        this.replacementMap = replacementMap;
        this.updatedFunctions = updatedFunctions;
        this.noiseRate=noiseRate;
    }

    public GatherCheckReply(AtomicInteger serviceNum, ACLMessage checkMsg, Boolean updated, String checkID) {
        this.serviceNum = serviceNum;
        this.requireCheckMessage = checkMsg;
        this.updated = updated;
        this.checkID = checkID;
    }

    //    private ACLMessage replyMsg;
    private MessageTemplate AnswerMT = MessageTemplate.and(MessageTemplate.MatchPerformative(ACLMessage.INFORM),
                                                           MessageTemplate.MatchConversationId("answer-capacity"));
    MessageTemplate updatedMT = MessageTemplate.and(MessageTemplate.MatchPerformative(ACLMessage.INFORM),
                                                    MessageTemplate.MatchConversationId(
                                                            "status-updated-" + checkID));

    @Override
    public void action() {
        String mAgentName = JadeUtil.getAgentName(myAgent.getAID());
        if (updated) {
            ACLMessage updateIF = myAgent.receive(updatedMT);
            if (updatedFunctions.get(mAgentName) == 1 || updateIF != null) {
                ACLMessage reply = new ACLMessage(ACLMessage.INFORM);
                reply.setConversationId("answer-capacity");
                CheckMessage replyMsg = new CheckMessage();
                try {
                    CheckMessage askMsg = mapper.readValue(requireCheckMessage.getContent(), CheckMessage.class);
//                    System.out.println(
//                            mAgentName + "已更新直接返回容量到：" + requireCheckMessage.getSender().getLocalName() + "-" + updatedFunctions.get(
//                                    mAgentName));
                    if (updatedFunctions.get(mAgentName) == 0) {
                        System.out.println("[error]updated flag should be 1 not 0");
                    }
//                    System.out.println("updatedFunctions:" + updatedFunctions);
                    replyMsg.setServiceNum(serviceNum.get());
                    replyMsg.setRelationType(askMsg.getRelationType());
                    reply.setContent(mapper.writeValueAsString(replyMsg));
                    reply.addReceiver(requireCheckMessage.getSender());
                    myAgent.send(reply);
                    step = 4;
                } catch (IOException e) {
                    throw new RuntimeException(e);
                }
            } else {
                block();
            }

        } else {
            switch (step) {
                case 1:
                    ACLMessage answerCapacity = myAgent.receive(AnswerMT);
                    if (answerCapacity != null) {
                        int sendNum = andRepliesNum + orRepliesNum + addRepliesNum;
                        int replyCnt = andRepliesCnt + orRepliesCnt + addRepliesCnt;
//                    if (myAgent.getLocalName().equals("中山大学第三附属医院-医院功能")) {
//                        System.out.println(
//                                "收到回信：" + answerCapacity.getSender().getLocalName() + "，还差" + (sendNum - replyCnt));
//                    }
                        String Content = answerCapacity.getContent();

                        CheckMessage answerCheckMsg;
                        try {
                            answerCheckMsg = mapper.readValue(Content, CheckMessage.class);
                        } catch (IOException e) {
                            throw new RuntimeException(e);
                        }
                        String relationType = answerCheckMsg.getRelationType();
                        String answerName = answerCapacity.getSender().getLocalName();
                        int Num = answerCheckMsg.getServiceNum();
                        String resourceType = null;
                        if (relationType.equals("add")) {
                            resourceType = answerCheckMsg.getResourceType();
                        }


//                    System.out.println(mAgentName + "收到邻居" + JadeUtil.getAgentName(
//                            answerCapacity.getSender()) + "的回信，类型为：" + type + ",容量为：" + Num);
                        if (relationType.equals("and")) {
                            if (andRepliesCnt == 0 || Num < andNum.get()) {
                                andNum.set(Num);
                            }
                            if (Num <= 0) {
                                failedNei.add(answerName);
                            } else {
                                availableNei.add(answerName);
                            }
                            andRepliesCnt++;
                        } else if (relationType.equals("or")) {
                            if (orRepliesCnt == 0 || Num > orNum.get()) {
                                if (Num > 0) {
                                    selectedAgg.clear();
                                    selectedAgg.put(answerCapacity.getSender().getLocalName(), Num);
                                }
//                            selectedAgg.delete(0, selectedAgg.length());
//                            selectedAgg.append(answerCapacity.getSender().getName());
                                orNum.set(Num);
//                            selectedAgg.put(selectedAggName,orNum.get());
                            }
                            if (Num <= 0) {
                                orFailedFun = answerName;
                            }
                            orRepliesCnt++;
                        } else if (relationType.equals("add")) {
                            if (resourceType.equals("high-quality") && Num > 0) {
                                highQualityRes.clear();
                                //可能有Bug
                                highQualityRes.put(answerCapacity.getSender().getLocalName(), Num);
                            } else if (resourceType.equals("low-cost") && Num > 0) {
                                lowCostRes.clear();
                                lowCostRes.put(answerCapacity.getSender().getLocalName(), Num);
                            }
                            addNum.set(addNum.get() + Num);
                            if (Num <= 0) {
                                addFailedFun = answerName;
                            }
                            addRepliesCnt++;
                        }
//                    else if (type.equals("replace")) {
//                        if (repRepliesCnt == 0 || Num > repFastNum.get()) {
//                            fastRep.delete(0, fastRep.length());
//                            fastRep.append(answerCapacity.getSender().getName());
//                            repFastNum.set(Num);
//                        }
//                        if (repRepliesCnt == 0 || Num < repQualityNum.get()) {
//                            qualityRep.delete(0, qualityRep.length());
//                            qualityRep.append(answerCapacity.getSender().getName());
//                            repQualityNum.set(Num);
//                        }
//                        repRepliesCnt++;
//                    }
//                    String askwerName = JadeUtil.getAgentName(answerCapacity.getSender());
//                    System.out.println(mAgentName + "收到邻居" +askwerName  + "的回信,类型为" + type + ",容量为：" + Num + ",andRepliesCnt：" + andRepliesCnt + ",orRepliesCnt：" + orRepliesCnt);
                        if (andRepliesCnt >= andRepliesNum && orRepliesCnt >= orRepliesNum && addRepliesCnt >= addRepliesNum) {
                            int num1 = Integer.MAX_VALUE, num2 = Integer.MAX_VALUE, num3 = Integer.MAX_VALUE;
                            if (andRepliesNum != 0) {
                                num1 = andNum.get();
//                            System.out.println(myAgent.getLocalName() + "-andNum:" + num1);
                            }

                            if (orRepliesNum != 0) {
                                num2 = orNum.get();
//                            System.out.println(myAgent.getLocalName() + "-orNum:" + num2);
                            }

                            if (addRepliesNum != 0) {
                                num3 = addNum.get();
//                            if (mAgentName.contains("医生值班")) {
//                                System.out.println("[自检]" + myAgent.getLocalName() + "的高质量资源为:" + highQualityRes);
//                                System.out.println("[自检]" + myAgent.getLocalName() + "的低消耗资源为:" + lowCostRes);
//                                System.out.println(myAgent.getLocalName() + "-addNum:" + num3);
//                            }

                            }
                            if (num2 == 0) {
                                failedNei.add(orFailedFun);
                            }
                            if (num3 == 0) {
                                failedNei.add(addFailedFun);
                            }
                            int min = (num1 < num2 ? num1 : num2) < num3 ? (num1 < num2 ? num1 : num2) : num3;
//                        System.out.println(myAgent.getLocalName() + "-min:" + min);
                            serviceNum.set(min);
//                        if (andRepliesNum != 0) {
//                            serviceNum.set(andNum.get());
//                        }
//                        if (orRepliesNum != 0) {
//                            serviceNum.set(Math.min(serviceNum.get(), orNum.get()));
//                        }
//                        if (addRepliesNum != 0) {
//                            serviceNum.set(Math.min(serviceNum.get(), addNum.get()));
//                            System.out.println(myAgent.getLocalName()+"的高质量资源为:" + highQualityRes);
//                            System.out.println(myAgent.getLocalName()+"的低消耗资源为:" + lowCostRes);
//                        }
                            if (andRepliesNum != 0 && orRepliesNum != 0 && addRepliesNum != 0) {
                                System.out.println("[自检]" + JadeUtil.getAgentName(myAgent) + ":缺少子节点！");
                            }
                            step = 3;
                        }
                    } else {
                        block();
                    }
                    break;
                case 2:
                    break;
                case 3:
                    int num = serviceNum.get();
                    String myName = myAgent.getLocalName();

                    if (replacementMap.containsKey(myName)) {
                        ArrayList<String> reps = replacementMap.get(myName);
                        if (num > 0) {
                            synchronized (replaceView) {
                                for (String rep : reps) {
                                    Set<String> s = replaceView.get(rep);
                                    if (s == null) {
                                        s = new HashSet<>();
                                        s.add(myName);
                                        if (myName.equals("外科ICU-医生值班")) {
                                            System.out.println("[替换视图]" + rep + "正在添加替换:" + myName);
                                        }
//
                                    } else if (!s.contains(myName)) {
                                        s.add(myName);
                                        if (myName.equals("外科ICU-医生值班")) {
                                            System.out.println("[替换视图]" + rep + "正在添加替换:" + myName);
                                        }
//                                    System.out.println("[替换视图]" + rep + "正在添加替换:" + myName);
                                    }

                                    replaceView.put(rep, s);
                                }
                            }
                        } else {
                            synchronized (replaceView) {
                                for (String rep : reps) {
                                    Set<String> s = replaceView.get(rep);
                                    if (s != null) {
                                        if (s.contains(myName)) {
                                            if (myName.equals("外科ICU-医生值班")) {
                                                System.out.println("[替换]" + rep + "的替换去除：" + myName);
                                            }

                                            s.remove(myName);
                                        }
                                        replaceView.put(rep, s);
                                    }
                                }
                            }
                        }

                    }
                    ACLMessage replyMsg = new ACLMessage(ACLMessage.INFORM);
                    CheckMessage requireCheckMsg;
                    try {
                        requireCheckMsg = mapper.readValue(requireCheckMessage.getContent(), CheckMessage.class);
                    } catch (IOException e) {
                        throw new RuntimeException(e);
                    }
                    String relationType = requireCheckMsg.getRelationType(); // and,or,add
                    String checkMode = requireCheckMsg.getCheckMode(); //check-replaceability or answer-capacity
                    int period = requireCheckMsg.getPeriod();
                    int requirementID = requireCheckMsg.getRequirementID();
                    int processID = requireCheckMsg.getProcessID();
                    String checkID = period + "-" + requirementID + "-" + processID;
                    if (checkMode.equals("replaceMode")) {
                        //为了保证收到信息后执行的行为是GatherAvailableReply中的case 4 而不是 GatherCheckReply
                        replyMsg.setConversationId("answer-capacity2Rep");//消息传递给GatherAvailableReply
                        String failedAgentName = requireCheckMsg.getFailedAgentName();
                        CheckMessage replyCheckMsg = new CheckMessage();
                        replyCheckMsg.setServiceNum(serviceNum.get());
                        replyCheckMsg.setCheckMode(checkMode);
                        replyCheckMsg.setFailedAgentName(failedAgentName);
                        try {
                            replyMsg.setContent(mapper.writeValueAsString(replyCheckMsg));
                        } catch (JsonProcessingException e) {
                            throw new RuntimeException(e);
                        }
                    } else {
                        //searchType.equals("normal") or searchType.equals("global")
                        replyMsg.setConversationId("answer-capacity");//消息传递给 GatherCheckReply
                        CheckMessage replyCheckMsg = new CheckMessage();
                        replyCheckMsg.setServiceNum(serviceNum.get());
                        replyCheckMsg.setRelationType(relationType);
                        try {
                            replyMsg.setContent(mapper.writeValueAsString(replyCheckMsg));
                        } catch (JsonProcessingException e) {
                            throw new RuntimeException(e);
                        }
                    }


                    replyMsg.addReceiver(requireCheckMessage.getSender());
                    if (myName.equals("血管外科-医生值班") && checkMode.equals("global")) {
                        String dir = JadeUtil.outputPath;
                        String fileName = "血管外科-医生值班-"+noiseRate+".txt";
                        append2file(dir + fileName,
                                    period + ":" + serviceNum.get() + "\n");
//                        System.out.println(myName + ":" + serviceNum.get());
                    }
                    if (myName.equals("眼科-医生值班") && checkMode.equals("global")) {
                        String dir = JadeUtil.outputPath;
                        String fileName = "眼科-医生值班-"+noiseRate+".txt";
                        append2file(dir + fileName,
                                    period + ":" + serviceNum.get() + "\n");
                    }
                    if (myName.equals("心血管内科-医生值班") && checkMode.equals("global")) {
                        String dir = JadeUtil.outputPath;
                        String fileName = "心血管内科-医生值班-"+noiseRate+".txt";
                        append2file(dir + fileName,
                                    period + ":" + serviceNum.get() + "\n");
                    }
                    synchronized (updatedFunctions) {
                        updatedFunctions.put(mAgentName, 1);
                    }
                    myAgent.send(replyMsg);
                    ACLMessage IFUpdated = new ACLMessage(ACLMessage.INFORM);
                    IFUpdated.setConversationId("status-updated-" + checkID);
                    IFUpdated.addReceiver(myAgent.getAID());
                    myAgent.send(IFUpdated);
//                System.out.println(
//                        mAgentName + "尝试回复状态给" + JadeUtil.getAgentName(checkMsg.getSender()) + "类型为：" + askType);
//                latestFlag.set(true);
                    step = 4;
                    break;
                case 4:
                    break;

            }
        }
//        replyMsg = checkMsg.createReply();


    }

    public static void append2file(String fileName, String content) {
        try {
            // 打开一个写文件器，构造函数中的第二个参数true表示以追加形式写文件
            FileWriter writer = new FileWriter(fileName, true);
            writer.write(content);
            writer.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    @Override
    public boolean done() {
        return (step == 4);
    }
}
