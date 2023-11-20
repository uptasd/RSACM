package resourceAgents;

import behaviours.reply.*;
import behaviours.reply.resource.ReplyResourceAvailability;
import behaviours.reply.resource.ReplyResourceStatus;
import functionAgents.AgentAttributes;
import jade.core.Agent;
import util.JadeUtil;

import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.atomic.AtomicInteger;

public class ResourceAgent extends Agent {
    //    public Boolean isResource=true;
//    public AtomicInteger neededNum=new AtomicInteger(0);
//    public AtomicBoolean decreasedFlag = new AtomicBoolean(false);
//    public AtomicBoolean increaseFlag = new AtomicBoolean(false);
//    public AtomicBoolean availableFlag = new AtomicBoolean(false);
    public AtomicInteger unavailableNum = new AtomicInteger(0);
    public AtomicInteger recoveryNum = new AtomicInteger(0);
    public String resourceType = "low-cost";
    public StringBuilder updateFlag = new StringBuilder("not-updated");
    private AtomicInteger serviceNum = new AtomicInteger();
    private String working_time = "8-18";
    private Map<Integer, Integer> periodStatus = new HashMap<>();

    @Override
    protected void setup() {
        ResourceBean arguments = (ResourceBean) getArguments()[0];
        int serviceCapacity = arguments.getServiceNum();
        working_time = arguments.getWorking_time();
        resourceType = arguments.getResourceType();
        serviceNum.set(serviceCapacity);
        AgentAttributes agentAttributes = new AgentAttributes()
                .unavailableNum(unavailableNum)
                .recoveryNum(recoveryNum)
                .updateFlag(updateFlag)
                .resourceType(resourceType)
                .working_time(working_time)
                .periodStatus(periodStatus)
                .serviceNum(serviceNum);

        addBehaviour(new ReplyResourceStatus(agentAttributes));
        addBehaviour(new ReplyResourceAvailability(agentAttributes));
        addBehaviour(new ReceiveDecreaseRequest(agentAttributes));
        addBehaviour(new ReceiveIncreaseRequest(agentAttributes));
        addBehaviour(new ReceiveEventRequest(agentAttributes));
//        doWait(10);

        JadeUtil.register_service(this, "resource", getLocalName());
//        System.out.println(getAID().getName() + "已加载，容量为:" + serviceCapacity);
    }
}
