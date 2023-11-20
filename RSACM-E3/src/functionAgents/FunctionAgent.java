package functionAgents;

import behaviours.reply.ReceiveDecreaseRequest;
import behaviours.reply.ReceiveIncreaseRequest;
import behaviours.reply.function.ReplyFunctionAvailability;
import behaviours.reply.function.ReplyFunctionStatus;
import jade.core.AID;
import jade.core.Agent;
import jade.domain.DFService;
import jade.domain.FIPAException;
import util.JadeUtil;

import java.util.*;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicInteger;

public class FunctionAgent extends Agent {
    public static final int Available = 1;
    public static final int Maintaining = 2;
    public static final int WaitRelease = 3;
    public static final int WaitMaintain = 3;
    public int DEFAULT_CAPACITY = 99;
    public ArrayList<AID> combFunction = new ArrayList<>();
    public ArrayList<AID> aggFunction = new ArrayList<>();
    public ArrayList<AID> depFunction = new ArrayList<>();
    //    public ArrayList<AID> repFunction = new ArrayList<>();
    public ArrayList<AID> resources = new ArrayList<>();
    public ArrayList<String> failedNei = new ArrayList<>();
    public ArrayList<String> availableNei = new ArrayList<>();
    public Map<String, Integer> selectedAgg = new HashMap<>();
    public Map<StringBuilder, Integer> highQualityRep = new HashMap<>();
    public Map<StringBuilder, Integer> lowCostRep = new HashMap<>();
    public Map<String, Integer> highQualityRes = new HashMap<>();
    public Map<String, Integer> lowCostRes = new HashMap<>();
    //    public AtomicBoolean decreasedFlag = new AtomicBoolean(false);
//    public AtomicBoolean increaseFlag = new AtomicBoolean(false);
    public AtomicBoolean availableFlag = new AtomicBoolean(false);
    public AtomicBoolean latestFlag = new AtomicBoolean(false);
    public AtomicInteger neededNum = new AtomicInteger(0);
    public AtomicInteger serviceNum = new AtomicInteger(DEFAULT_CAPACITY);
    public Deque<List<String>> offerDeque = new LinkedList<>();
    public StringBuilder updateFlag = new StringBuilder("not-updated");
    public int status;
    public int maxCapacity = DEFAULT_CAPACITY;
    public static Map<String, ArrayList<String>> replacementMap = null;
    public static Map<String, Set<String>> replaceView = null;
    public static Map<String, Integer> updatedFunctions = null;
    AgentAttributes agentAttributes;
    AtomicInteger last_serviceNum = new AtomicInteger();

    @Override
    protected void setup() {
//        if (getLocalName().equals("中山大学第三附属医院-住院登记")) {
//            System.out.println("load");
//        }

        Map<String, List> neighbors = (Map<String, List>) getArguments()[0];
        List<String> dep_agents = neighbors.get("dep_agents");
        List<String> agg_agents = neighbors.get("agg_agents");
        List<String> res_agents = neighbors.get("res_agents");
        replacementMap = (Map<String, ArrayList<String>>) getArguments()[1];
        replaceView = (Map<String, Set<String>>) getArguments()[2];
        updatedFunctions = (Map<String, Integer>) getArguments()[3];
//        if(neighbors.containsKey("rep_agents")){
//            List<String> rep_agents = neighbors.get("rep_agents");
//            for (String agent_name : rep_agents) {
//                repFunction.add(new AID(agent_name,AID.ISLOCALNAME));
//            }
//        }
        for (String agent_name : dep_agents) {
            depFunction.add(new AID(agent_name, AID.ISLOCALNAME));
        }
        for (String agent_name : agg_agents) {
            aggFunction.add(new AID(agent_name, AID.ISLOCALNAME));
        }
        for (String agent_name : res_agents) {
            resources.add(new AID(agent_name, AID.ISLOCALNAME));
        }
        agentAttributes = new AgentAttributes()
                .serviceNum(serviceNum)
//                .offerDeque(offerDeque)
//                .decreasedFlag(decreasedFlag)
//                .increaseFlag(increaseFlag)
                .availableFlag(availableFlag)
//                .neededNum(neededNum)
                .selectedAgg(selectedAgg)
                .highQualityRep(highQualityRep)
                .lowCostRep(lowCostRep)
                .highQualityRes(highQualityRes)
                .lowCostRes(lowCostRes)
//                .latestFlag(latestFlag)
                .updateFlag(updateFlag)
                .depFunction(depFunction)
                .aggFunction(aggFunction)
                .failedNei(failedNei)
                .availableNei(availableNei)
                .replaceView(replaceView)
                .replacementMap(replacementMap)
                .updatedFunctions(updatedFunctions)
                .last_serviceNum(last_serviceNum)
                .resources(resources);
//                .replacementMap(replacementMap);
//        System.out.println(getAID().getName() + "已加载");
        addBehaviour(new ReplyFunctionStatus(agentAttributes));
        addBehaviour(new ReplyFunctionAvailability(agentAttributes));
        addBehaviour(new ReceiveDecreaseRequest(agentAttributes));
        addBehaviour(new ReceiveIncreaseRequest(agentAttributes));
//        addBehaviour(new ReplyFunctionReplaceability(agentAttributes));
//        if(dep_agents.size()!=0){
//            System.out.println("dep_agent:"+dep_agents);
//        }
//        if(agg_agents.size()!=0){
//            System.out.println("agg_agents:"+agg_agents);
//        }
//        if(res_agents.size()!=0){
//            System.out.println("res_agents:"+res_agents);
//        }
        doWait(1);
        //这个得延迟注册，否则有可能会导致agent还没初始化就开始注册服务了，不过偶尔还是会出现这个bug
        JadeUtil.register_service(this,
                                  "Function", getLocalName());
    }

    protected void takeDown() {
        // Printout a dismissal message
//        System.out.println(getAID().getName() + " terminating.");
        try {
            DFService.deregister(this);
        } catch (FIPAException e) {
            throw new RuntimeException(e);
        }
    }
}
