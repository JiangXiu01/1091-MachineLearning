# For Python 2 / 3 compatability
from __future__ import print_function
import csv
import pandas as pd 
from os import listdir
from os.path import isfile, join
import pickle
import numpy as np 
# Toy Loglistset.
# Format: each row is an example.
# The last column is the label.
# The first two columns are features.
# Feel free to play with it by adding more features & examples.
# Interesting note: I've written this so the 2nd and 5th examples
# have the same features, but different labels - so we can see how the
# tree handles this case.


def loaddata(what):

    #匯入log清單
    dirpath = 'D:/高科大學校/機器學習/MLGame-master8.01/MLGame-master/games/pingpong/log'
    files = listdir(dirpath)
    Loglist = []

    for f in files:
        fullpath = join(dirpath, f)
        loadFile = open(fullpath, "rb")
        Loglist.append(pickle.load(loadFile))
        loadFile.close()
        
    #匯入Log資料
    Frame = []    
    status = []
    BallPosition = []
    Ballspeed = []
    PlatformPosition_1P = []
    PlatformPosition_2P = []

    for i in range(0, len(Loglist)):
        for j in range(0, len(Loglist[i]['ml_1P']['scene_info'])):
            Frame.append(Loglist[i]['ml_1P']['scene_info'][j]['frame'])
            status.append(Loglist[i]['ml_1P']['scene_info'][j]['status'])
            BallPosition.append(Loglist[i]['ml_1P']['scene_info'][j]['ball'])
            Ballspeed.append(Loglist[i]['ml_1P']['scene_info'][j]['ball_speed'])
            PlatformPosition_1P.append(Loglist[i]['ml_1P']['scene_info'][j]['platform_1P'])
            PlatformPosition_2P.append(Loglist[i]['ml_2P']['scene_info'][j]['platform_2P'])
    print('Ballspeed長度',len(Ballspeed))    
    print('log檔數量',len(Loglist))        
    #DL = 1 , DR = 2 , UL = 3 , UR = 4
    LRUP = []
    ball_to_200 = 0
    ball_to_plat = []
    ballx = 0
    bally = 0  
    next_x = np.array(np.zeros((len(Frame))))
    next_x = next_x - 1
    
    if(what == '1P'):#load1P
        for i in range(0, len(Loglist)):
            for j in range(0, len(Loglist[i]['ml_1P']['scene_info'])):
                print(i,j)
                if(Loglist[i]['ml_1P']['scene_info'][j]['ball_speed'][0] < 0):#向左
                    if(Loglist[i]['ml_1P']['scene_info'][j]['ball_speed'][1] < 0):#向上
                        #going up
                        ball_to_200 = 200 - int(Loglist[i]['ml_1P']['scene_info'][j]['ball'][0])
                        LRUP.append(np.array((3,ball_to_200)))
                     #   LRUP.append(np.array((Ballspeed - Loglist[i].ball[0],(Ballspeed - Loglist[i].ball[1]))))
                        qwe = len(LRUP)-1
                        next_x[qwe] = 10
                            
                        #U.L

                    else:
                        #going down
                        ball_to_200 = 200 - int(Loglist[i]['ml_1P']['scene_info'][j]['ball'][0])
                        LRUP.append(np.array((1,ball_to_200)))
                      #  LRUP.append(np.array((Ballspeed - Loglist[i].ball[0],(Ballspeed - Loglist[i].ball[1]))))
                        if(Loglist[i]['ml_1P']['scene_info'][j]['ball'][1] > Loglist[i]['ml_1P']['scene_info'][j]['platform_1P'][1] - 40):
                            ballx = Loglist[i]['ml_1P']['scene_info'][j]['ball'][0]
                            bally = Loglist[i]['ml_1P']['scene_info'][j]['ball'][1]
                            while(bally < Loglist[i]['ml_1P']['scene_info'][j]['platform_1P'][1]):
                                ballx -= 1
                                bally += 1
                            if(ballx < 0):
                                ballx = np.abs(ballx)
                            if(ballx >= 170):
                                ballx = np.round(ballx/10) +1
                            elif(ballx <= 30):
                                ballx = np.round(ballx/10) -1
                            else:
                                ballx = np.round(ballx/10)
                            qwe = len(LRUP)-1
                            while(next_x[qwe] == -1 and qwe >= 0):
                                next_x[qwe] = ballx
                                qwe -= 1
                        #DL

                else:
                    if(Loglist[i]['ml_1P']['scene_info'][j]['ball_speed'][1] < 0):
                        #going up
                        ball_to_200 = 200 - int(Loglist[i]['ml_1P']['scene_info'][j]['ball'][0])
                        LRUP.append(np.array((4,ball_to_200)))
                        #LRUP.append(np.array((Ballspeed - Loglist[i].ball[0],(Ballspeed - Loglist[i].ball[1]))))
                        qwe = len(LRUP)-1
                        next_x[qwe] = 10
                        #U.R

                    else:
                        #going down
                        ball_to_200 = 200 - int(Loglist[i]['ml_1P']['scene_info'][j]['ball'][0])
                        LRUP.append(np.array((2,ball_to_200)))
                        #LRUP.append(np.array((Ballspeed - Loglist[i].ball[0],(Ballspeed - Loglist[i].ball[1]))))
                        if(Loglist[i]['ml_1P']['scene_info'][j]['ball'][1] > Loglist[i]['ml_1P']['scene_info'][j]['platform_1P'][1]-40):
                            ballx = Loglist[i]['ml_1P']['scene_info'][j]['ball'][0]
                            bally = Loglist[i]['ml_1P']['scene_info'][j]['ball'][1]
                            while(bally < Loglist[i]['ml_1P']['scene_info'][j]['platform_1P'][1]):
                                ballx += 1
                                bally += 1
                            if(ballx > 200):
                                ballx = 400 - ballx
                            if(ballx >= 170):
                                ballx = np.round(ballx/10) +1
                            elif(ballx <= 30):
                                ballx = np.round(ballx/10) -1
                            else:
                                ballx = np.round(ballx/10)
                            qwe = len(LRUP)-1
                            while(next_x[qwe] == -1 and qwe >= 0):
                                next_x[qwe] = ballx
                                qwe -= 1
                        #D.R.
    
    
    else:
        #load 2P
        for i in range(0, len(Loglist)):
            for j in range(0, len(Loglist[i]['ml_1P']['scene_info'])):
                print(i,j)
                if(Loglist[i]['ml_1P']['scene_info'][j]['ball_speed'][0] < 0):#向左
                    if(Loglist[i]['ml_1P']['scene_info'][j]['ball_speed'][1] < 0):#向上
                            #going down
                            ball_to_200 = 200 - int(Loglist[i]['ml_1P']['scene_info'][j]['ball'][0])
                            LRUP.append(np.array((3,ball_to_200)))
                         #   LRUP.append(np.array((Ballspeed - Loglist[i].ball[0],(Ballspeed - Loglist[i].ball[1]))))
                            qwe = len(LRUP)-1
                            next_x[qwe] = 10
                                
                            #D.L
        
                    else:
                        #going up
                        ball_to_200 = 200 - int(Loglist[i]['ml_1P']['scene_info'][j]['ball'][0])
                        LRUP.append(np.array((1,ball_to_200)))
                      #  LRUP.append(np.array((Ballspeed - Loglist[i].ball[0],(Ballspeed - Loglist[i].ball[1]))))
                        if(Loglist[i]['ml_1P']['scene_info'][j]['ball'][1] < 120):
                            ballx = Loglist[i]['ml_1P']['scene_info'][j]['ball'][0]
                            bally = Loglist[i]['ml_1P']['scene_info'][j]['ball'][1]
                            while(bally > 80):
                                ballx -= 1
                                bally -= 1
                            if(ballx < 0):
                                ballx = np.abs(ballx)
                            if(ballx >= 170):
                                ballx = np.round(ballx/10) +1 
                            elif(ballx <= 30):
                                ballx = np.round(ballx/10) -1
                            else:
                                ballx = np.round(ballx/10)
                            qwe = len(LRUP)-1
                            if(np.abs(ballx*10 - (Loglist[i]['ml_1P']['scene_info'][j]['platform_2P'][0] + 20)) <= 25):
                                ballx = ballx
                            else:
                                ballx = np.round((Loglist[i]['ml_1P']['scene_info'][j]['platform_2P'][0] + 20)/10)
                            while(next_x[qwe] == -1 and qwe >= 0):
                                next_x[qwe] = ballx
                                qwe -= 1
                        #UL
    
                else:
                    if(Loglist[i]['ml_1P']['scene_info'][j]['ball'][1] > 0):
                        #going down
                        ball_to_200 = 200 - int(Loglist[i]['ml_1P']['scene_info'][j]['ball'][0])
                        LRUP.append(np.array((4,ball_to_200)))
                        #LRUP.append(np.array((Ballspeed - Loglist[i].ball[0],(Ballspeed - Loglist[i].ball[1]))))
                        qwe = len(LRUP)-1
                        next_x[qwe] = 10
                        #D.R
    
                    else:
                        #going up
                        ball_to_200 = 200 - int(Loglist[i]['ml_1P']['scene_info'][j]['ball'][0])
                        LRUP.append(np.array((2,ball_to_200)))
                        #LRUP.append(np.array((Ballspeed - Loglist[i].ball[0],(Ballspeed - Loglist[i].ball[1]))))
                        if(Loglist[i]['ml_1P']['scene_info'][j]['ball'][1] < 120):
                            ballx = Loglist[i]['ml_1P']['scene_info'][j]['ball'][0]
                            bally = Loglist[i]['ml_1P']['scene_info'][j]['ball'][1]
                            while(bally > 80):
                                ballx += 1
                                bally -= 1
                            if(ballx > 200):
                                ballx = 400 - ballx
                            if(ballx >= 170):
                                ballx = np.round(ballx/10) +1
                            elif(ballx <= 30):
                                ballx = np.round(ballx/10) -1
                            else:
                                ballx = np.round(ballx/10)
                            qwe = len(LRUP)-1
                            if(np.abs(ballx*10 - (Loglist[i]['ml_1P']['scene_info'][j]['platform_2P'][0] + 20)) <= 25):
                                ballx = ballx
                            else:
                                ballx = np.round((Loglist[i]['ml_1P']['scene_info'][j]['platform_2P'][0] + 20)/10)
                            while(next_x[qwe] == -1 and qwe >= 0):
                                next_x[qwe] = ballx
                                qwe -= 1
                        #U.R.
    
    ball_to_plat =  np.array(ball_to_plat[:-1])
    Ballarray = np.array(BallPosition[:-1])
    LRUP = np.array((LRUP[:-1]))
    x = np.hstack((Ballarray,LRUP))    
    y = next_x[:-1]    
    from sklearn.model_selection import train_test_split
    x_train,x_test,y_train,y_test = train_test_split(x,y,test_size = 0.1,random_state = 41)
    training_data = np.hstack((x_train,y_train[:,np.newaxis]))
    testing_Loglist = np.hstack((x_test,y_test[:,np.newaxis]))
    for i in range(0,10):
        print(training_data[i*15])
    return training_data

#---------------------------------------


# Column labels.
# These are used only to print the tree.
# header = ["ball_x", "ball_y", "LRUP", "ballto200", "next_x"]

def unique_vals(rows, col):
    """Find the unique values for a column in a Loglistset."""
    return set([row[col] for row in rows])


def class_counts(rows):
    """Counts the number of each type of example in a Loglistset."""
    counts = {}  # a dictionary of label -> count.
    for row in rows:
        # in our Loglistset format, the label is always the last column
        label = row[-1]
        if label not in counts:
            counts[label] = 0
        counts[label] += 1
    return counts


def is_numeric(value):
    """Test if a value is numeric."""
    return isinstance(value, int) or isinstance(value, float)



class Question:
    """A Question is used to partition a Loglistset.

    This class just records a 'column number' (e.g., 0 for Color) and a
    'column value' (e.g., Green). The 'match' method is used to compare
    the feature value in an example to the feature value stored in the
    question. See the demo below.
    """

    def __init__(self, column, value):
        self.column = column
        self.value = value

    def match(self, example):
        # Compare the feature value in an example to the
        # feature value in this question.
        val = example[self.column]
        if is_numeric(val):
            return val >= self.value
        else:
            return val == self.value

    def __repr__(self):
        # This is just a helper method to print
        # the question in a readable format.
        condition = "=="
        if is_numeric(self.value):
            condition = ">="
        return "Is %s %s %s?" % (
            header[self.column], condition, str(self.value))
        


def partition(rows, question):
    """Partitions a Loglistset.

    For each row in the Loglistset, check if it matches the question. If
    so, add it to 'true rows', otherwise, add it to 'false rows'.
    """
    true_rows, false_rows = [], []
    for row in rows:
        if question.match(row):
            true_rows.append(row)
        else:
            false_rows.append(row)
    return true_rows, false_rows


def gini(rows):
    
    counts = class_counts(rows)
    impurity = 1
    for lbl in counts:
        prob_of_lbl = counts[lbl] / float(len(rows))
        impurity -= prob_of_lbl**2
    return impurity




def info_gain(left, right, current_uncertainty):
    """Information Gain.

    The uncertainty of the starting node, minus the weighted impurity of
    two child nodes.
    """
    p = float(len(left)) / (len(left) + len(right))
    return current_uncertainty - p * gini(left) - (1 - p) * gini(right)



def find_best_split(rows):
    """Find the best question to ask by iterating over every feature / value
    and calculating the information gain."""
    best_gain = 0  # keep track of the best information gain
    best_question = None  # keep train of the feature / value that produced it
    current_uncertainty = gini(rows)
    n_features = len(rows[0]) - 1  # number of columns

    for col in range(n_features):  # for each feature

        values = set([row[col] for row in rows])  # unique values in the column

        for val in values:  # for each value

            question = Question(col, val)

            # try splitting the Loglistset
            true_rows, false_rows = partition(rows, question)

            # Skip this split if it doesn't divide the
            # Loglistset.
            if len(true_rows) == 0 or len(false_rows) == 0:
                continue

            # Calculate the information gain from this split
            gain = info_gain(true_rows, false_rows, current_uncertainty)

            # You actually can use '>' instead of '>=' here
            # but I wanted the tree to look a certain way for our
            # toy Loglistset.
            if gain >= best_gain:
                best_gain, best_question = gain, question

    return best_gain, best_question



class Leaf:
    """A Leaf node classifies Loglist.

    This holds a dictionary of class (e.g., "Apple") -> number of times
    it appears in the rows from the training Loglist that reach this leaf.
    """

    def __init__(self, rows):
        self.predictions = class_counts(rows)
        
class Decision_Node:
    """A Decision Node asks a question.

    This holds a reference to the question, and to the two child nodes.
    """

    def __init__(self,
                 question,
                 true_branch,
                 false_branch):
        self.question = question
        self.true_branch = true_branch
        self.false_branch = false_branch
    def classify_test(self,row):
        """See the 'rules of recursion' above."""
        node = self
        # Base case: we've reached a leaf
        if isinstance(node, Leaf):
            return node.predictions
    
        # Decide whether to follow the true-branch or the false-branch.
        # Compare the feature / value stored in the node,
        # to the example we're considering.
        if node.question.match(row):
            return classify(row, node.true_branch)
        else:
            return classify(row, node.false_branch)
 
def build_tree(rows):
    """Builds the tree.

    Rules of recursion: 1) Believe that it works. 2) Start by checking
    for the base case (no further information gain). 3) Prepare for
    giant stack traces.
    """

    # Try partitioing the Loglistset on each of the unique attribute,
    # calculate the information gain,
    # and return the question that produces the highest gain.
    gain, question = find_best_split(rows)

    # Base case: no further info gain
    # Since we can ask no further questions,
    # we'll return a leaf.
    if gain == 0:
        return Leaf(rows)

    # If we reach here, we have found a useful feature / value
    # to partition on.
    true_rows, false_rows = partition(rows, question)

    # Recursively build the true branch.
    true_branch = build_tree(true_rows)

    # Recursively build the false branch.
    false_branch = build_tree(false_rows)

    # Return a Question node.
    # This records the best feature / value to ask at this point,
    # as well as the branches to follow
    # dependingo on the answer.
    return Decision_Node(question, true_branch, false_branch)

def print_tree(node, spacing=""):
    """World's most elegant tree printing function."""
#    fp = open("my_tree.txt", "a")

    # Base case: we've reached a leaf
    if isinstance(node, Leaf):
        print (spacing + "Predict", node.predictions)
#        str123 = str(spacing) + "Predict", str(node.predictions) + "\n"
#        fp.write(str(str123))
        return
    # Print the question at this node
    print (spacing + str(node.question))
#    str123 = str(spacing) + str(node.question) + "\n"
#    fp.write(str(str123))
    # Call this function recursively on the true branch
    print (spacing + '--> True:')
#    str123 = str(spacing) + "--> True:" + "\n"
#    fp.write(str(str123))
    print_tree(node.true_branch, spacing + "  ")
    # Call this function recursively on the false branch
    print (spacing + '--> False:')
#    str123 = str(spacing) + "--> False:" + "\n"
#    fp.write(str(str123))
    print_tree(node.false_branch, spacing + "  ")
#    fp.close()


#print_tree(my_tree)

def classify(row, node):
    """See the 'rules of recursion' above."""

    # Base case: we've reached a leaf
    if isinstance(node, Leaf):
        return node.predictions

    # Decide whether to follow the true-branch or the false-branch.
    # Compare the feature / value stored in the node,
    # to the example we're considering.
    if node.question.match(row):
        return classify(row, node.true_branch)
    else:
        return classify(row, node.false_branch)

def classify_test(row):
    """See the 'rules of recursion' above."""
    node = my_tree
    # Base case: we've reached a leaf
    if isinstance(node, Leaf):
        return node.predictions

    # Decide whether to follow the true-branch or the false-branch.
    # Compare the feature / value stored in the node,
    # to the example we're considering.
    if node.question.match(row):
        return classify(row, node.true_branch)
    else:
        return classify(row, node.false_branch)

def print_leaf(counts):
    """A nicer way to print the predictions at a leaf."""
    total = sum(counts.values()) * 1.0
    probs = {}
    for lbl in counts.keys():
        probs[lbl] = str(int(counts[lbl] / total * 100)) + "%"
    return probs


if __name__ == "__main__":
    what = '2P'
    if(what == '1P'):
        my_tree = build_tree(loaddata('1P'))   
        filename = "my_tree_beta801_1P_new.sav"
    else:
        my_tree = build_tree(loaddata('2P'))   
        filename = "my_tree_beta801_2P_new.sav"
    pickle.dump(my_tree,open(filename,"wb"))
