import datetime
import time
import sys
import os
 
def usage():
    print('''Help Information:
             kmsg_translate inputfile:   input file  to parse        
                        ''')
if len(sys.argv) < 2:
    usage()
    sys.exit(2)

inpath = sys.argv[1]
print(inpath)
 
def calc_delta(stream):
    global s_second
    global s_microsecond
    global a_time

    if a_time ==None:
        print("Can't convert to android time")
        exit(-1)
    for line in stream:
        if line:
            try:
                begin_index =  line.index('[')
                end_index = line[begin_index+1:].index(']')+begin_index+1
                time_string = line[begin_index + 1 :end_index]

                [d_second,d_microsecond] = time_string.split('.')

                delta_second = int(int(d_second) - int(s_second))
                delta_microsecond = int(int(d_microsecond)-int(s_microsecond))

                [t_second, t_microsecond] = a_time.split('.')
                seconds = (delta_second + int(t_second))
                microseconds = (delta_microsecond + int(t_microsecond) * 1000)
                if microseconds < 0:
                    microseconds = microseconds + 1000000
                    seconds = seconds - 1

                times = str(seconds)
                x = time.localtime(float(times))
                realtime = time.strftime('%Y-%m-%d %H:%M:%S', x)
                new_line = realtime+ "." + str(microseconds) +' ' + line

                outputfile.write(new_line)
            except:
                outputfile.write(line)
 
def get_atime(stream):
    global s_second
    global s_microsecond
    global a_time

    for line in stream:
        if line:
            match_string = 'UTC;android time '
            a_time_op = line.find(match_string)
            if a_time_op>=1:
                begin_index =  line.index('[')
                end_index = line[begin_index+1:].index(']')+begin_index+1

                date_string = line[a_time_op + len(match_string) :]

                abs_time = line[begin_index + 1 :end_index].strip()
                [s_second,s_microsecond] = abs_time.split('.')
                a_time = date_string.strip()

                print("begin_index: " + str(begin_index))
                print("end_index: " + str(end_index))
                print("date_string: " + str(date_string.strip()))
                print("abs_time: " + str(abs_time))
                print("s_second " + str(s_second))
                print("s_microsecond " + str(s_microsecond))
                print("a_time " + str(a_time))

                [t_second, t_microsecond] = a_time.split('.')
                t_second = time.mktime(datetime.datetime.strptime(t_second, "%Y-%m-%d %H:%M:%S").timetuple())
                # a_time = str(t_second + 8 * 60 * 60) + t_microsecond
                a_time = str(t_second).split('.')[0] + "." + t_microsecond
                print("a_time " + a_time)

                break
 
def main():
    global inputfile
    global outputfile

    if inpath == None:
        usage()
        sys.exit(2)

    inputfile = open(inpath, 'r')
    outputfile = open(os.getcwd() + '/' + inpath + '_translated', 'w')

    get_atime(inputfile)

    inputfile.seek(0)
    calc_delta(inputfile)

    inputfile.close()
    outputfile.close()

if __name__ == "__main__":
    main()
