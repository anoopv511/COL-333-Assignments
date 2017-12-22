import java.util.Scanner;
import java.util.Map;
import java.util.Arrays;
import java.util.ArrayList;
import java.util.LinkedList;
import java.util.HashMap;
import java.util.Vector;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.PrintWriter;

// FBS Class
public class fbs{

    public Map<String,frame> all_frames;

    // FBS Constructor
    public fbs(){
        this.all_frames = new HashMap<String,frame>();
        Scanner fbs_in = new Scanner(System.in);
        Boolean quit = false;
        System.out.println("Enter 0 to read from file");
        System.out.println("Enter 1 to add new Frame");
        System.out.println("Enter 2 to update existing Frame");
        System.out.println("Enter 3 to delete existing Frame");
        System.out.println("Enter 4 to query a Frame");
        System.out.println("Enter 5 to print all Frame names");
        System.out.println("Enter 6 to save to file");
        System.out.println("Enter q to quit");
        while(!quit){
            System.out.print("-> ");
            String in = fbs_in.nextLine();
            switch(in){
                case "0":
                    System.out.print("Enter file name - ");
                    String file_in = fbs_in.nextLine();
                    read_fromFile(file_in);
                    break;
                case "1":
                    add_frame(fbs_in,false);
                    break;
                case "2":
                    System.out.print("\tEnter frame name - ");
                    String f_name1 = fbs_in.nextLine();
                    update_frame(f_name1,fbs_in);
                    break;
                case "3":
                    System.out.print("\tEnter frame name - ");
                    String f_name2 = fbs_in.nextLine();
                    delete_frame(f_name2);
                    break;
                case "4":
                    query_frame_byname(fbs_in,"");
                    break;
                case "5":
                    print_f_names();
                    break;
                case "6":
                    System.out.print("Enter file name - ");
                    String file_out = fbs_in.nextLine();
                    save_toFile(file_out);
                    break;
                case "q":
                    quit = true;
                    break;
                default:
                    System.out.println("Enter proper option");
                    break;
            }
        }
        fbs_in.close();
    }

    // Method to read Frames from File
    public void read_fromFile(String filename){
        try{
            Scanner fbs_file_in = new Scanner(new File(filename));
            while(fbs_file_in.hasNextLine()){
                add_frame(fbs_file_in,true);
                // System.out.println("\t-----------------");
            }
            fbs_file_in.close();
        }catch(FileNotFoundException fx){
            fx.printStackTrace();
        }
    }

    // Method to save Frames to File
    public void save_toFile(String filename){
        try{
            PrintWriter writer = new PrintWriter(filename,"UTF-8");
            for(frame f : this.all_frames.values()) writer.write(f.file_out());
            writer.close();
        }catch(Exception x){
            x.printStackTrace();
        }
    }

    // Method to add new Frames to FBS
    public void add_frame(Scanner f_in,Boolean fromFile){
        frame f = new frame(f_in,fromFile);
        this.all_frames.put(f.f_name,f);
        // f.print_frame("\t");
    }
    
    // Method to update existing Frames of FBS
    public void update_frame(String f_name,Scanner f_in){
        frame f = this.all_frames.get(f_name);
        if(f == null) return;
        f.print_frame("\t\t");
        Boolean quit = false;
        System.out.println("\tEnter 1 to add/update slot of selected frame");
        System.out.println("\tEnter 2 to delete slot of the selected frame");
        System.out.println("\tEnter q to quit");
        while(!quit){
            System.out.print("\t--> ");
            String in = f_in.nextLine();
            switch(in){
                case "1":
                    System.out.print("\tSlot : Value - ");
                    String slot_val = f_in.nextLine();
                    String[] slot_val_split = slot_val.split("\\s*:\\s*");
                    String slot_name = slot_val_split[0];
                    String value = slot_val_split[1];
                    f.update_slot(slot_name,frame.make_val_type(slot_name,value));
                    break;
                case "2":
                    System.out.print("\tSlot - ");
                    String slot_name_d = f_in.nextLine();
                    f.delete_slot(slot_name_d);
                    break;
                case "q":
                    quit = true;
                    break;
                default:
                    System.out.println("\tEnter proper option");
                    break;
            }
        }
        this.all_frames.put(f.f_name,f);
    }

    // Method to delete Frames from FBS
    // Deletes Frame and its subtree
    public void delete_frame(String f_name){
        frame f = this.all_frames.get(f_name);
        if(f == null) return;
        f.print_frame("\t\t");
        LinkedList<String> delete_frames = new LinkedList<String>();
        delete_frames.add(f.f_name);
        while(delete_frames.size() != 0){
            frame x = this.all_frames.get(delete_frames.poll());
            for(Map.Entry<String,frame> i : this.all_frames.entrySet()){
                if(i.getValue().parent != null && i.getValue().parent.equals(x.f_name)){
                    delete_frames.add(i.getKey());
                }
            }
            this.all_frames.remove(x.f_name);
        }
    }

    // Method to List all Frames in FBS
    public void print_f_names(){
        for(String name : this.all_frames.keySet()) System.out.println("\t" + name);
    }

    // Method to query Frame of FBS by Name
    // Returns Frame with its own slots and also those of its parents
    public frame query_frame_byname(Scanner f_in,String print_format){
        System.out.print(print_format + "\tEnter Frame Name - ");
        String f_name = f_in.nextLine();
        frame base_frame = this.all_frames.get(f_name);
        if(base_frame == null){
            System.out.println("\tNo frame with given name");
            return null;
        }
        LinkedList<frame> frame_queue = new LinkedList<frame>();
        frame_queue.add(base_frame);
        frame parent_frame = frame_queue.peekLast().parent != null ? all_frames.get(frame_queue.peekLast().parent) : null;
        while(parent_frame != null){
            frame_queue.add(parent_frame);
            parent_frame = frame_queue.peekLast().parent != null ? all_frames.get(frame_queue.peekLast().parent) : null;
        }
        frame out_frame = new frame();
        out_frame.f_name = base_frame.f_name;
        while(frame_queue.size() != 0){
            frame f = frame_queue.removeLast();
            for(Map.Entry<String,pair<ArrayList<String>,String>> slot : f.slots.entrySet()){
                String slot_name = slot.getKey().toLowerCase();
                if(!(slot_name.equals("ako") || slot_name.equals("inst") || slot_name.equals("a_part_of"))){
                    out_frame.update_slot(slot_name,slot.getValue());
                }
            }
        }
        String parent_slot = base_frame.slots.get("ako") != null ? "ako" : (base_frame.slots.get("inst") != null ? "inst" : (base_frame.slots.get("a_part_of") != null) ? "a_part_of" : null);
        if(parent_slot != null) out_frame.update_slot(parent_slot,base_frame.slots.get(parent_slot));
        out_frame.parent = base_frame.parent;
        out_frame.print_frame(print_format + "\t");
        return out_frame;
    }

    public static void main(String[] args){
        fbs sys = new fbs();
    }

}

// Frame Class
class frame{

    public String f_name;
    public Map<String,pair<ArrayList<String>,String>> slots;
    public String parent;

    // Frame Constructor
    public frame(Scanner f_in,Boolean fromFile){
        this.slots = new HashMap<String,pair<ArrayList<String>,String>>();
        if(!fromFile) System.out.print("\t\tEnter Frame Name - ");
        this.f_name = f_in.nextLine();
        if(!fromFile) System.out.println("\t\tEnter q to quit adding slots to the Frame");
        Boolean quit = false;
        while(!quit){
            if(!fromFile) System.out.print("\t\t---> ");
            String in = f_in.nextLine();
            switch(in){
                case "q":
                    quit = true;
                    break;
                case "---":
                    quit = true;
                    break;
                default:
                    if(!fromFile) System.out.print("\t\tSlot : Value - ");
                    String slot_val = !fromFile ? f_in.nextLine() : in;
                    String[] slot_val_split = slot_val.split("\\s*:\\s*");
                    String slot_name = slot_val_split[0];
                    String value = slot_val_split[1];
                    update_slot(slot_name,make_val_type(slot_name,value));
                    break;
            }
        }
    }

    public frame(){
        this.f_name = "";
        this.slots = new HashMap<String,pair<ArrayList<String>,String>>();
        this.parent = "";
    }

    public frame(String f_name,Map<String,pair<ArrayList<String>,String>> slots,String parent){
        this.f_name = f_name;
        this.slots = new HashMap<String,pair<ArrayList<String>,String>>(slots);
        this.parent = parent;
    }

    public frame(frame f){
        this.f_name = f.f_name;
        this.slots = new HashMap<String,pair<ArrayList<String>,String>>(f.slots);
        this.parent = f.parent;
    }

    public static pair<ArrayList<String>,String> make_val_type(String slot_name,String value){
        pair<ArrayList<String>,String> val_type = new pair<ArrayList<String>,String>(new ArrayList<String>(Arrays.asList(value.replaceAll("\\[|\\]","").split("\\s*,\\s*"))),"None");
        String[] split_val = value.split("\\s*=\\s*");
        String type_check = split_val[0].toLowerCase();
        if(type_check.equals("default")){
            val_type.first = new ArrayList<String>(Arrays.asList(split_val[1].replaceAll("\\[|\\]","").split("\\s*,\\s*")));
            val_type.second = "Default";
        }
        else if(type_check.equals("range")){
            val_type.first = new ArrayList<String>(Arrays.asList(split_val[1].split("\\s*,\\s*")));
            val_type.second = "Range";
        }
        else if(slot_name.equals("ako") || slot_name.equals("a_part_of") || slot_name.equals("inst")){
            val_type.second = "Parent";
        }        
        return val_type;
    }

    // Method to print Frame properly
    public void print_frame(String print_format){
        System.out.println(print_format + "Frame Name - " + this.f_name);
        System.out.println(print_format + "Slot - [Value, Type]");
        for(Map.Entry<String,pair<ArrayList<String>,String>> slot : this.slots.entrySet()){
            String val = slot.getValue().first.size() == 1 ? slot.getValue().first.get(0) : slot.getValue().first.toString();
            System.out.println(print_format + slot.getKey() + " - [" + val + ", " + slot.getValue().second + "]");
        }
    }

    public String file_out(){
        String out = this.f_name + "\n";
        for(Map.Entry<String,pair<ArrayList<String>,String>> slot : this.slots.entrySet()){
            String val_string = slot.getValue().first.toString();
            String val = slot.getValue().first.size() == 1 ? slot.getValue().first.get(0) : (slot.getValue().second.equals("Range") ? val_string.subSequence(1,val_string.length()).toString() : val_string);
            out = out + slot.getKey() + " : " + val + "\n";
        }
        out = out + "---\n";
        return out;
    }

    // Method to add/update slots of Frame
    public void update_slot(String slot_name,pair<ArrayList<String>,String> val_type){
        this.slots.put(slot_name,val_type);
        String slot_name_lower = slot_name.toLowerCase();
        if(slot_name_lower.equals("ako") || slot_name_lower.equals("a_part_of") || slot_name_lower.equals("inst")){
            this.parent = val_type.first.get(0);
        }
    }

    // Method to delete slots of Frame
    public void delete_slot(String slot_name){
        this.slots.remove(slot_name);
        String slot_name_lower = slot_name.toLowerCase();
        if(slot_name_lower.equals("ako") || slot_name_lower.equals("a_part_of") || slot_name_lower.equals("inst")){
            this.parent = null;
        }
    }

}

class pair<S,T>{

    public S first;
    public T second;

    public pair(S s,T t){
        this.first = s;
        this.second = t;
    }

}