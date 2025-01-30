import java.io.*;
import java.lang.reflect.Array;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.*;

public class MP1 {
    Random generator;
    String userName;
    String delimiters = " \t,;.?!-:@[](){}_*/";
    String[] stopWordsArray = {"i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours",
            "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its",
            "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that",
            "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having",
            "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while",
            "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before",
            "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again",
            "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each",
            "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than",
            "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"};

    public MP1(String userName) {
        this.userName = userName;
    }


    public Integer[] getIndexes() throws NoSuchAlgorithmException {
        Integer n = 10000;
        Integer number_of_lines = 50000;
        Integer[] ret = new Integer[n];
        long longSeed = Long.parseLong(this.userName);
        this.generator = new Random(longSeed);
        for (int i = 0; i < n; i++) {
            ret[i] = generator.nextInt(number_of_lines);
        }
        return ret;
    }
	
	// Taken directly from top solution (with minor modification for reverse order sort): https://stackoverflow.com/questions/109383/sort-a-mapkey-value-by-values
	public class MapUtil {
		public static <K, V extends Comparable<? super V>> Map<K, V> sortByValue(Map<K, V> map) {
			List<Map.Entry<K, V>> list = new ArrayList<>(map.entrySet());
			list.sort(Collections.reverseOrder(Map.Entry.comparingByValue()));
			Map<K, V> result = new LinkedHashMap<>();
			for (Map.Entry<K, V> entry : list) {
				result.put(entry.getKey(), entry.getValue());
			}

			return result;
		}
	}

	public String[] process() throws Exception{
		String[] topItems = new String[20];
		Integer[] indexes = getIndexes();

		//TO DO
		// Enter data using BufferReader
		BufferedReader r = new BufferedReader(new InputStreamReader(System.in));

		int lineCount = 0;
		String[] titles = new String[50000];
		String s = r.readLine();
		while(s != null) {	
			titles[lineCount++] = s;
			s = r.readLine();
		}
		r.close();

		Map <String, Integer> wordCounts = new HashMap<>();
		for(int index : indexes) {
			//tokenizing title based on delimiters
			//String[] words = titles[index].split(delimiters);
			String[] words = titles[index].split("[ \t,;\\.\\?\\!\\-:@\\[\\]\\(\\)\\{\\}_*/]");
			//count words in the title, ignoring words in stopWordsArray
			for(String word : words) {
				String wordNWSLC = word.toLowerCase().replaceAll("\\s+","");
				if(wordNWSLC != "" && !Arrays.asList(stopWordsArray).contains(wordNWSLC) && wordCounts.containsKey(wordNWSLC)) {
					wordCounts.put(wordNWSLC, wordCounts.get(wordNWSLC) + 1);
				}
				else if (wordNWSLC != "" && !Arrays.asList(stopWordsArray).contains(wordNWSLC)) {
					wordCounts.put(wordNWSLC, 1);
				}
			}
		}
		
		/* for (Map.Entry<String, Integer> entry : wordCounts.entrySet()) {
			System.out.println(entry.getKey() + " " + entry.getValue());
		} */
		
		Map<String, Integer> sortedWordCounts = MapUtil.sortByValue(wordCounts);
		//Map<String, Integer> sortedWordCounts = sortByValueOrIfTiedByKey(wordCounts);
		
		Map<Integer, ArrayList<String>> sortedWordCountsInvertedMap = new TreeMap<>(Collections.reverseOrder());
		for (Map.Entry<String, Integer> entry : sortedWordCounts.entrySet()) {
			if(sortedWordCountsInvertedMap.containsKey(entry.getValue())) {
					sortedWordCountsInvertedMap.get(entry.getValue()).add(entry.getKey());
				}
				else {
					sortedWordCountsInvertedMap.put(entry.getValue(), new ArrayList<String>());
					sortedWordCountsInvertedMap.get(entry.getValue()).add(entry.getKey());
				}
		}
		
		int returnCount = 0;
		/* for (Map.Entry<String, Integer> entry : sortedWordCounts.entrySet()) {
			if(returnCount == 20) {
				break;
			}
			//System.out.println(entry.getKey() + " " + entry.getValue());
			topItems[returnCount++] = entry.getKey();
		} */
		for (Map.Entry<Integer, ArrayList<String>> entry : sortedWordCountsInvertedMap.entrySet()) {
			Collections.sort(entry.getValue());
			for(String word : entry.getValue()) {
				//System.out.println(word + " " + entry.getKey());
				topItems[returnCount++] = word;
				if(returnCount == 20) {
					return topItems;
				}
			}
		}
		return topItems;
    }

    public static void main(String args[]) throws Exception {
    	if (args.length < 1){
    		System.out.println("missing the argument");
    	}
    	else{
    		String userName = args[0];
	    	MP1 mp = new MP1(userName);
	    	String[] topItems = mp.process();

	        for (String item: topItems){
	            System.out.println(item);
	        }
	    }
	}

}

// REFERENCES
// https://www.geeksforgeeks.org/ways-to-read-input-from-console-in-java/
// https://www.geeksforgeeks.org/bufferedreader-readline-method-in-java-with-examples/
// https://stackoverflow.com/questions/5071040/java-convert-integer-to-string
// https://stackoverflow.com/questions/5455794/removing-whitespace-from-strings-in-java
// https://www.google.com/search?q=make+lowercase+java&rlz=1C1CHBF_enUS1071US1071&oq=make+lowercase+java&gs_lcrp=EgZjaHJvbWUyCQgAEEUYORiABDIHCAEQABiABDIHCAIQABiABDIHCAMQABiABDIHCAQQABiABDIHCAUQABiABDIHCAYQABiABDIHCAcQABiABDIHCAgQABiABDIHCAkQABiABNIBCDI1NDBqMGo3qAIAsAIA&sourceid=chrome&ie=UTF-8
// https://stackoverflow.com/questions/1348199/what-is-the-difference-between-the-hashmap-and-map-objects-in-java\
// https://stackoverflow.com/questions/4157972/how-to-update-a-value-given-a-key-in-a-hashmap
// https://www.w3schools.com/jsref/jsref_includes_array.asp
// https://www.geeksforgeeks.org/sorting-a-hashmap-according-to-values/
// https://stackoverflow.com/questions/59924699/for-loops-and-arrays-in-java
// https://stackoverflow.com/questions/1128723/how-do-i-determine-whether-an-array-contains-a-particular-value-in-java
// https://www.google.com/search?q=iterating+through+first+x+elements+of+a+map+java&rlz=1C1CHBF_enUS1071US1071&oq=iterating+through+first+x+elements+of+a+map+java&gs_lcrp=EgZjaHJvbWUyCQgAEEUYORigATIHCAEQIRigATIHCAIQIRifBTIHCAMQIRifBdIBCDcxMTJqMGo3qAIAsAIA&sourceid=chrome&ie=UTF-8
// https://stackoverflow.com/questions/14134558/list-of-all-special-characters-that-need-to-be-escaped-in-a-regex
// https://medium.com/sina-ahmadi/java-regex-6e4d073aab85
// https://stackoverflow.com/questions/53325650/what-is-the-type-of-map-entry-comparingbyvalue-reversed
// https://stackoverflow.com/questions/79379449/reading-from-stdin-via-bufferedreader-in-while-loop-array-only-correct-if-syst